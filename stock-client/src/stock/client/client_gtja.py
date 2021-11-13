import os
import time

import win32process
import xlrd
from pywinauto import timings, mouse, keyboard
import pywinauto as pw
import pandas as pd
from pywinauto.findwindows import WindowNotFoundError

from src.img_code.cut_image import ImgType
from src.stock.bean.stock_bean import Account, PopupResult, PositionType, Money, remove_code_prefix, StockInfo, StockResult
from src.stock.client.base_client import WindowType
from src.stock.client.base_client_tdx import BaseClientTDX, conf, log, get_handle
from src.utils import windows_utils as wu
from src.utils.code_utils import code_to_str


# 国泰君安
class ClientGtja(BaseClientTDX):
    """
    注意：
        1. 交易设置：输入框股票代码自动显示   取消
        2. 交易设置：买入价格，卖出价格  -> 不锁定
        3. 程序设置：锁屏保护时间：999 分钟，读公告信息时间: 3秒
        4. 当日成交(F6):  包含撤单成交  -> 取消
        5.
    取消自动升级：

    """

    def _after_init(self):
        self._main_hwnd = get_handle("富易", conf.exe_gtja)
        if self._main_hwnd is None:
            self._main_hwnd = get_handle("国泰君安证券|富易登录", conf.exe_gtja)

        thread_id, process_id = win32process.GetWindowThreadProcessId(self._main_hwnd)
        self._app = pw.Application(backend="win32").connect(process=process_id)
        log.info("启动%s，句柄：%x,进程ID:%x", "国泰君安-富易", self._main_hwnd, process_id)

        self._main_window = self._app.window(title_re="%s.+" % "富易")
        self._trade_window = self._main_window.TspSkinPanel7

    def _is_login(self, account: Account) -> bool:
        return self._main_window.exists() and self._main_window.is_visible()

    def _change_account(self, account: Account) -> bool:
        self._max_window()
        return True

    def _login_account(self, account: Account) -> bool:
        login_window = self._app.window(title="国泰君安证券|富易登录")
        pwd_edit = login_window.Edit3
        pwd_edit.set_focus()
        pwd_edit.set_text("")
        wu.press(*account.password)

        try:
            login_window.type_keys("{ENTER}")
            timings.wait_until(30, 0.5, lambda: self._trade_window.exists() and self._trade_window.is_visible())
        except Exception as e:
            log.exception(e)
        login_success = self._is_login(account)
        if login_success:
            self._refresh_window()
        return login_success

    @staticmethod
    def support_brokers() -> list:
        return ["国泰君安"]

    def _select_window(self, window_type):
        self._close_popup_windows()  # 关闭所有弹框
        self._max_window()
        w = self._get_window_conf()[window_type]
        self._main_window.type_keys(w.get("item"))  # 跳转到买入页面

    def _get_window_conf(self):
        return {WindowType.W_BUY: {"item": "{F2}"},
                WindowType.W_SELL: {"item": "{F3}"},
                WindowType.W_CANCEL: {"item": "{F8}"},
                WindowType.W_POSITION: {"item": "{F4}"},
                WindowType.W_DEAL: {"item": "{F6}"},
                WindowType.W_ENTRUST: {"item": "{F8}"},
                }

    # 导出数据
    def _out_data(self, opt_window, file_path) -> bool:
        for i in range(2):
            try:
                self.__close_save_as()
                self._max_window()
                self._click_tool_bar(opt_window, 'out')
                self._save_file(file_path)
                return True
            except Exception as e:
                log.info("界面：%s, 导出数据异常，重试：%d/%d", opt_window, i + 1, 2)
                log.exception(e)
        return False

    def _save_file(self, file_path):
        file_path = self._to_xls(file_path)
        file_dialog = self._app.window(title="另存为", top_level_only=True, visible_only=True)
        if not file_dialog.exists():
            raise WindowNotFoundError("没有找到输出窗口！")

        # 如果文件存在
        if os.path.exists(file_path):
            os.remove(file_path)
            log.info("删除文件------%s", file_path)

        path_name, file_name = os.path.dirname(file_path), os.path.basename(file_path)

        # 重新设置保存路径
        path_edit = file_dialog.child_window(title_re="地址:.*", class_name="ToolbarWindow32")
        if (path_edit.window_text().replace("地址: ", "")).lower() != path_name.lower():
            path_edit.set_focus()
            p = path_edit.rectangle()
            mouse.click(coords=(p.right - 30, p.top + 18))
            keyboard.send_keys("{BACKSPACE}" + path_name + "{ENTER}")
            time.sleep(0.1)
        # 设置文件名
        file_dialog.Edit.set_text(file_name)
        file_dialog['保存(&S)'].click_input()
        time.sleep(0.2)

    def _to_xls(self, file_path: str):
        return os.path.splitext(file_path)[0] + ".xls"

    # 点击功能按钮
    def _click_tool_bar(self, opt_window, btn_type):
        p_right = {'out': 20, "flash": 120}
        w_type = {"_position_window": "TZQDrzjgpPage", "_deal_window": "TZQDrcjPage", "_entrust_window": "TZQWtcdPage"}
        p = self._main_window[w_type.get(opt_window)].rectangle()
        time.sleep(0.1)
        mouse.click(coords=(p.right - p_right[btn_type], p.top + 20))

    # 读取导出的文件
    def _read_file(self, file_path, head_line=5, position_type: PositionType = None, encoding="GBK", pre_callback=None,
                   **pd_kwargs) -> pd.DataFrame:
        file_path = self._to_xls(file_path)
        if os.path.exists(file_path):
            head_line = 8 if position_type == PositionType.CHI_CHANG else 5
            skipfooter = 1 if position_type == PositionType.CHI_CHANG else 0
            df = pd.read_excel(xlrd.open_workbook(file_path, encoding_override="gbk"), header=head_line, skipfooter=skipfooter)
            df.rename(columns=lambda x: x.strip(), inplace=True)  # 删除列名中空格
            df.dropna(subset=["证券代码"], inplace=True)
            log.info("账号：%s，%s查询结果:%s", self.account, position_type.name, df)
            return df
        else:
            raise FileNotFoundError("文件：%s不存在！", file_path)

    # 读取资金信息
    def _get_money(self, file_path) -> Money:
        file_path = self._to_xls(file_path)
        if os.path.exists(file_path):
            with xlrd.open_workbook(file_path, encoding_override="gbk") as workbook:
                sheet = workbook.sheet_by_index(0)
                total_assets = sheet.cell_value(6, 4)
                available = sheet.cell_value(6, 1)
                return Money(total_assets=total_assets, available=available)
        else:
            log.warn("获取账户资金失败，文件:%s不存在！", file_path)
        return Money(total_assets=.0, available=.0)

    def _close_message_dialog(self):
        """
        关闭消息中心弹框
        :return: None
        """
        try:
            msg_dialog = self._app.window(title_re="消息.*")
            if msg_dialog.exists(timeout=1.5) and msg_dialog.is_visible():
                msg_dialog.close()
                log.debug("关闭消息中心！")
        except:
            pass

    def __close_save_as(self):
        # 关闭另存为窗口
        try:
            file_dialogs = self._app.windows(title="另存为", top_level_only=True)
            for fd in file_dialogs:
                fd.close()
        except:
            pass

    def sell(self, stock_info: StockInfo) -> StockResult:
        try:
            sell_window = self.__open_buy_or_sell(WindowType.W_SELL)
            codeEdit = sell_window.child_window(class_name="TspCustomEdit")
            codeEdit.set_text("")
            codeEdit.type_keys(remove_code_prefix(stock_info.code))
            time.sleep(0.2)
            sell_window.Edit5.set_text(stock_info.price)
            sell_window.Edit3.set_text(stock_info.number)
            sell_window.child_window(title="限价卖出(&S)", class_name="TspSkinButton").click_input()
            time.sleep(0.2)
            p = PopupResult(self._close_popup_windows(), regex=self._get_contract_regex())
            log.info("账号：%s，委托卖出(%s)，股票：%s，价格:%.2f, 股数：%d，合同编号：%s, 结果：%s",
                     self.account, p.is_success(), stock_info.code, stock_info.price, stock_info.number, p.contract, p.texts)
            self._close_message_dialog()
            return StockResult.result_ok(p.contract) if p.is_success() else StockResult.result_error(p.text)
        except Exception as e:
            self._close_popup_windows()
            log.exception(e)
            return StockResult.result_error(str(e))

    def buy(self, stock_info: StockInfo) -> StockResult:
        try:
            buy_window = self.__open_buy_or_sell(WindowType.W_BUY)
            codeEdit = buy_window.child_window(class_name="TspCustomEdit")
            codeEdit.set_text("")
            codeEdit.type_keys(remove_code_prefix(stock_info.code))
            time.sleep(0.2)
            buy_window.Edit5.set_text(stock_info.price)
            buy_window.Edit3.set_text(stock_info.number)
            buy_window.child_window(title="限价买入(&B)", class_name="TspSkinButton").click_input()
            time.sleep(0.2)
            p = PopupResult(self._close_popup_windows(), regex=self._get_contract_regex())
            log.info("账号：%s，委托买入(%s)，股票：%s，价格:%.2f, 股数：%d，合同编号: %s, 结果：%s",
                     self.account, p.is_success(), stock_info.code, stock_info.price, stock_info.number, p.contract, p.texts)
            self._close_message_dialog()
            return StockResult.result_ok(p.contract) if p.is_success() else StockResult.result_error(p.text)
        except Exception as e:
            self._close_popup_windows()
            log.exception(e)
            return StockResult.result_error(str(e))

    def __open_buy_or_sell(self, w_type):
        w_name = {WindowType.W_BUY: "TZQBuyPage2", WindowType.W_SELL: "TZQSellPage2"}
        for i in range(2):
            try:
                self._select_open_window(w_type)
                w_window = self._main_window[w_name.get(w_type)]
                timings.wait_until(2, 0.1, lambda: w_window.exists() and w_window.is_visible())
                return w_window
            except timings.TimeoutError as e:
                log.info("账号：%s，打开窗口：%s，失败，准备重试！%s", self.account, w_type, str(e))

    # 获取弹框信息
    def _get_popup_info(self, popup_window):
        try:
            panel = popup_window.child_window(class_name="TspSkinPanel")
            if panel.exists(timeout=1) and panel.is_visible():
                panel.set_focus()
                panel.click_input()
                if panel.exists(timeout=0.5) and panel.is_visible():
                    text = str(code_to_str(panel.rectangle(), ImgType.text, lang="chi_sim", enhance=1)).replace(' ', '').replace("\n", " ")
                    log.debug(text)
                    return popup_window.window_text(), text if "自动化操作软件!" not in text else ""
            return None, None
        except Exception as e:
            log.exception(e)
            log.error(str(e))
            self._close_message_dialog()
        return None, None

    def _get_contract_regex(self):
        """
         合同编号获取正则表达式
         """
        return ".*合同号为:?(\\d+).*"

    def cancel_all(self) -> bool:
        try:
            self._select_open_window(WindowType.W_CANCEL)
            self.__cancel_submit("%{A}")
            return True
        except Exception as e:
            log.exception(e)
            return False

    def cancel(self, stock_codes: [] = None, entrust_nos: [] = None, cancel_type=None, exception_callback=None, **kwargs) -> bool:
        try:
            p_list = self.position(position_type=PositionType.WEI_TUO)
            if p_list and len(p_list) > 0:
                list_view = self._main_window.TZQWtcdPage.TAdvStringGrid
                select_indexs = []
                for obj in self._is_cancel(p_list, stock_codes, entrust_nos, cancel_type):
                    select_indexs.append(obj.index)
                    log.debug("账号：%s，准备撤销：%s", self.account, obj)

                log.debug("账号：%s，需要撤销的委托数量为：%d", self.account, len(select_indexs))
                for index in select_indexs:
                    top = index * 32 + int(32 / 2) + 32
                    list_view.click(coords=(5, top))
                if len(select_indexs) > 1:
                    self.__cancel_submit("%{R}")
                elif len(select_indexs) == 1:
                    self.cancel_all()
            return True
        except Exception as e:
            log.exception(e)
        return False

    def __cancel_submit(self, key=None):
        if key:
            keyboard.send_keys(key)
        time.sleep(0.3)
        keyboard.send_keys("{ENTER}")
        time.sleep(0.3)
        self._close_message_dialog()
        self._close_popup_windows()

    def _close_popup_windows(self, timeout: float = -0.1, handle_map=None, close_foreach=False) -> dict:
        self._close_message_dialog()
        result = super()._close_popup_windows(timeout=timeout, handle_map=handle_map, close_foreach=close_foreach)
        return result


if __name__ == '__main__':
    from src.utils.log import init_log

    init_log("xiadan.log", "xiadan")
    a = Account(username='111', password='222', type=1, brokers="22", nickname="22")
    o = ClientGtja(a)
    # o._close_message_dialog()
    # o._close_popup_windows()
    # print(o.position(PositionType.WEI_TUO, retry=1))
    # print(o.money())
    # o.buy(StockInfo("601398", 1, price="5.03", amount=100))
    # o.sell(StockInfo("601398", 1, price="5.03", amount=100))
    o.cancel()
    # o.cancel_all()
