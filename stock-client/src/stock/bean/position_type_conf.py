from src.stock.bean.stock_bean import PositionType, StockPosition, StockDeal, StockEntrust

brokers_conf = {
    "default": {
        PositionType.POSITION: {
            "map": {
                "stockCode": "证券代码",
                "stockName": "证券名称",
                "totalNum": ["实际数量", "当前拥股数", "持仓数量", "证券数量", "当前持仓", "股票余额", "当前可拥股数"],  # 总数量
                "sellNum": ["可用余额", "可用数量", "可卖数量", "可用股份"],  # 可卖数量
                "freezeNum": ["冻结数量"],  # 冻结数量
                "costPrice": ["成本价", "参考成本价", "买入成本价"],  # 成本价
                "currentPrice": ["市场价", "当前价", "参考市价", "市价"],  # 市场价、当前价
                "marketValue": ["市值", "最新市值", "证券市值"],  # 市值
                "profitLoss": ["盈亏", "浮动盈亏", "参考盈亏"],  # 盈亏
                "profitLossRatio": ["盈亏比(%)", "盈亏比例(%)"],  # 盈亏比
                "todayProfitLoss": ["当日盈亏"],  # 当日盈亏
                "todayProfitLossRatio": ["当日盈亏比(%)"],  # 当日盈亏比
                "stockHolder": ["股东帐户", "股东代码"],  # 股东代码
                "tradingMarket": ["交易市场"],  # 交易市场

            },
            "type": StockPosition
        },
        PositionType.DEAL: {
            "map": {
                "stockCode": "证券代码",
                "stockName": "证券名称",
                "dealDate": "成交日期",
                "dealTime": "成交时间",  # 成交时间
                "num": "成交数量",  # 成交数量
                "price": ["成交均价", "成交价格"],  # 成交价格
                "money": "成交金额",  # 成交金额
                "type": ["操作", "委托类别", "买卖标志", "买卖", "方向"],  # 买卖标志
                "dealNo": ["成交编号",  "流水号"],  # 成交编号
                "entrustNo": ["委托编号", "合同编号"],  # 委托编号
                "stockHolder": ["股东代码", "股东帐户", "股东账户"],  # 股东代码
                "tradingMarket": ["交易市场"],  # 交易市场
            },
            "type": StockDeal
        },
        PositionType.ENTRUST: {
            "map": {
                "stockCode": "证券代码",
                "stockName": "证券名称",
                "entrustNo": ["合同编号", "委托编号"],  # 委托编号
                "entrustDate": ["委托日期"],  # 委托日期
                "entrustTime": ["委托时间"],  # 委托时间
                "type": ["操作", "委托类别", "买卖标志", "买卖"],  # 委托类型（证券买入、证券卖出，买入，卖出）
                "num": "委托数量",  # 委托数量
                "price": "委托价格",  # 委托价格
                "dealNum": "成交数量",  # 成交数量
                "dealPrice": ["成交均价", "成交价格"],  # 成交均价
                "stockHolder": ["股东帐户", "股东代码"],  # 股东代码
                "tradingMarket": ["交易市场"],  # 交易市场
                "remark": ["备注", "状态说明", "委托状态", "状态"],
                "cancelNum": ["撤消数量", "撤单数量", "已撤数量"],  # 撤单数量
            },
            "type": StockEntrust
        }
    },
    "东方财富": {
        PositionType.POSITION: {
            "map": {
                "sellNum": "库存数量",
            },
        },
    },
    "英大证券": {
        PositionType.POSITION: {
            # 证券代码，证券名称，证券数量，可卖数量，参考摊薄成本价，当前价，最新市值，参考摊薄保本价，参考摊薄浮动盈亏，冻结数量，非流通数量，非流通市值，股东代码，参考盈亏比例(%)
            "map": {
                "costPrice": "参考摊薄成本价",
                "profitLoss": "参考摊薄浮动盈亏",
                "profitLossRatio": "参考盈亏比例(%)"
            },
        },
    },
    "国海证券": {
        PositionType.POSITION: {
            "map": {
                "marketValue": "最新价",
            },
            "type": StockPosition
        },
        PositionType.DEAL: {
            "map": {
                "type": "买卖方向",
            },
            "type": StockDeal
        },
        PositionType.ENTRUST: {
            "map": {
                "type": "买卖方向",
            },
            "type": StockEntrust
        }
    }
}


def __merge_config(conf_map, default_config, position_type) -> dict:
    """
    合并配置信息，主要是用特斯配置覆盖默认配置
    @param conf_map: 特斯配置
    @param default_config: 默认配置
    @param position_type: 配置类型
    @return:
    """
    if position_type not in conf_map:
        return dict(default_config[position_type])
    target = dict(conf_map[position_type])
    target['type'] = default_config[position_type]['type']
    for k, v in default_config[position_type]['map'].items():
        if k not in target['map']:
            target['map'][k] = v
    return target


def get_brokers_conf(brokers, position_type: PositionType) -> dict:
    """
    获取持仓，委托，成交，字段对应关系
    :param brokers: 证券公司列表
    :param type: 仓位类型
    :return:
    """
    conf_map = brokers_conf["default"]
    brokers = brokers if isinstance(brokers, list) else [brokers]
    for broker in brokers:
        if broker in brokers_conf:
            conf_map = brokers_conf[broker]
            break

    if position_type in conf_map:
        return __merge_config(conf_map, brokers_conf["default"], position_type)
    return dict(brokers_conf["default"][position_type])


if __name__ == '__main__':
    print(get_brokers_conf("国海证券", PositionType.DEAL))
    print(get_brokers_conf("东方财富", PositionType.POSITION))
    print(get_brokers_conf("东方财富", PositionType.DEAL))
    print(get_brokers_conf("招商证券", PositionType.POSITION))
