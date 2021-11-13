package com.ruoyi.stock.utils;

import java.util.Arrays;
import java.util.List;

import lombok.extern.slf4j.Slf4j;

/**
 * @author bestitxq
 * @date 2019/4/3 14:25
 */
@Slf4j
public class MaxDrawdownUtils {

	/**
	 * 计算最大回撤:某段时间内连续收益率之和最小的值为最大回撤
	 * @param rates：收益率
	 * @return 最大回撤
	 */
	public static double calculateByIncrease(List<Double> rates) {
		double s = 0;
		double e = 0;
		double max = 0;
		double temp = 0;
		double ts = 0;
		// 收益率不为空
		if (!rates.isEmpty()) {
			for (int i = 0; i < rates.size(); i++) {
				// 获得收益率
				double r = rates.get(i);
				temp = temp + r;
				if (temp > 0) {
					ts = i + 1;
					e = i + 1;
					temp = 0;
				} else {
					if (temp < max) {
						s = ts;
						e = i;
						max = temp;
					}
				}
			}
		}
		log.info("最大回撤计算结果：maxsum={},start={}，end={}", max, s, e);
		return max;
	}

	/**
	 * 按照资金计算最大回撤
	 * @param equityValues 资金信息
	 * @return 最大回撤
	 */
	public static double calculateByMoney(List<Double> equityValues) {
		if (equityValues == null || equityValues.size() < 2)
			return 0;

		double maxDrawdown = 0; // 最大回撤
		double maxEquityValue = equityValues.get(0); // 当日之前的最大资产净值

		for (int i = 1; i < equityValues.size(); i++) {
			double currentEquityValue = equityValues.get(i); // 当日资产净值
			double drawDown = (1 - currentEquityValue / maxEquityValue);
			maxDrawdown = Math.max(maxDrawdown, drawDown);

			maxEquityValue = Math.max(currentEquityValue, maxEquityValue);
		}
		log.info("calMaxDrawdown最大回撤计算结果：{}", maxDrawdown);
		return maxDrawdown;
	}

	public static void main(String[] args) {
		Double[] c = {0.026316,0.048433,-0.067935,0.037901,0.030899};
		calculateByIncrease(Arrays.asList(c));
		Double[] c2 = {3.42,3.51,3.68,3.43,3.56,3.67};
		calculateByMoney(Arrays.asList(c2));
	}
}
