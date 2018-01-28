package arima;

import java.io.*;
import java.math.BigDecimal;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Scanner;

import com.alibaba_inc.odpsmr.Statistics;

public class test1 {

	public static void main(String args[]) {

		long millisPerDay = 24 * 3600 * 1000;
		SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd");

		Scanner ino = null;

		try {

			List<Long> Y = new ArrayList<Long>();

			// ino=new Scanner(new
			// File("D:\\0c80008b0a28d356026f4b1097041689.txt"));
			ino = new Scanner(new File(
					"D:\\11e08a9c88682aaa9c98b6b79c9a5fbc.csv"));
			// ino=new Scanner(new
			// File("D:\\0693f5e1c570d9678523c41e03aae3ab.txt"));

			while (ino.hasNext()) {
				// System.out.println(ino.next().split(",")[0]);
				String[] strs = ino.next().split(",");

				Y.add(Long.parseLong(strs[0]));
				System.out.println(Long.parseLong(strs[0]));
			}

			System.out.println("---------");
			
			System.out.println(predict2(Y));
			
			System.out.println(Statistics.getMin(Y));
			System.out.println(Statistics.getMax(Y));
			
			// 平滑
			for (int i = 0; i < 5; ++i)
				Y = weightSmooth(Y);
			for (int i = 0; i < 3; ++i)
				Y = weightSmooth2(Y);
			
			System.out.println("predict:"+exponentialSmooth(Y.subList(Y.size()-21, Y.size()),1.0/7));
			
			

			// 获得基方差
			long offset = Statistics.getStandardDiviation(Y);
			long predictVal = predict(Y);
//			if(true){ // 97fd17d25cddbe4f97a826c84157a4d7
//				predictVal += offset;
//			}
			
			System.out.println(predictVal);

		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			ino.close();
		}

	}
	
	public static Long predict2(List<Long> Y) {
		
		int useDays = 28; // 四周
		double rate = 1.0/7;
		
		// 最后有波峰
		long peekRate = 3;
		int index = 0;
		for(int i=Y.size()-1;i>=1;--i){
			if((Y.get(i) >= peekRate * Y.get(i-1)) // 迅速增加
					|| (Y.get(i-1) >= peekRate * Y.get(i))){ // 迅速降低
				index = i;
				System.out.println(index);
				break;
			}
		}
		
		// 截断
		int stableNum = Y.size() - index;
		
		System.out.println(stableNum);
		if(stableNum<10){ // 不足10天,最后有波峰
			if(stableNum>7)
				rate = 0.07;
			else if(stableNum>5)
				rate = 0.01;
			else if(stableNum>3)
				rate = 0.1;
			else if(stableNum==2) // 2,3
				rate = 0.3;
			else
				rate = 0.5;
			
			Y = exponentialSmooth(Y.subList(Y.size()-useDays, Y.size()),rate);
			return Y.get(Y.size()-1); // 最后一个
			
//			List<Long> beforeY = Y.subList(index-14,index); // 前14天
//			long avgBeforeY = Statistics.getAverage(beforeY);
//		
//			List<Long> afterY = Y.subList(index,Y.size()); // 后几天
//			long avgAfterY = Statistics.getAverage(afterY);
//		
//			long predictY = (long)(avgBeforeY * 0.6 + avgAfterY * 0.4);
//			
//			return predictY;
			
		}	
		
		// 明显递增或者递减
		long minY = Statistics.getMin(Y);
		long maxY = Statistics.getMax(Y);
		long lastY = Y.get(Y.size()-1); 
		if(lastY==minY||lastY==maxY){ 
			if(stableNum>10) // 如果是逐渐递增的则返回
				return lastY;
		}
		
		
		
		for (int i = 0; i < 5; ++i)
			Y = weightSmooth(Y);
		for (int i = 0; i < 3; ++i)
			Y = weightSmooth2(Y);
		
		// 最后几天预测
//		long sum = 0;
//		long days = 7;
//		for(int i=1;i<=days;++i){
//			sum+= Y.get(Y.size() - i);
//		}
//		return sum/days;
		
		
		Y = exponentialSmooth(Y.subList(Y.size()-useDays, Y.size()),rate);
		return Y.get(Y.size()-1); // 最后一个
		
	}
	
	

	public static Long predict(List<Long> Y) {

		// 最后几天预测值
//		long sum = 0;
//		long days = 7;
//		for (int i = 1; i <= days; ++i) {
//			sum += Y.get(Y.size() - i);
//		}
//		long predictBase = sum / days;

		int daysForAvg = 14;
		double maxChangIndex = 0.15;
		
		int daysForTrend = 56;
		int trendPeriod = 1;
		
		
		
		long offset = Statistics.getStandardDiviation(Y.subList(Y.size()-daysForAvg, Y.size()));
		long predictBase = Statistics.getAverage(Y.subList(Y.size()-daysForAvg, Y.size()));
		
		// 波动太大的返回平滑值
		double changeIndex = offset * 1.0 / predictBase;
		if (changeIndex > maxChangIndex){
			return predictBase;
		}
		

		// 14天一个周期采样
		List<Long> lsAvgs = new ArrayList<Long>();
		Y = Y.subList(Y.size()-daysForTrend, Y.size());
		
		for (int i = Y.size() - 1; i - trendPeriod >= 0; i -= trendPeriod) {
			long avg = Statistics.getAverage(Y.subList(i - trendPeriod, i));
			lsAvgs.add(avg);
		}
		// 从后往前，再倒转，按时间顺序
		Collections.reverse(lsAvgs);

		
		// 存放拟合合理的值
		List<Long> reasonableY = new ArrayList<Long>();

		//lsAvgs = weightSmooth(lsAvgs);
		
		
		// 2,3 拟合
		for (int order = 2; order <= 5; ++order) {
			long predictY = LeastSquareMethod.getNextY(lsAvgs, order);
			System.out.println("order: "+predictY);
			if (Math.abs(predictY - predictBase) <= offset) {
				reasonableY.add(predictY);
			}
		}
		// 趋势判断
		double trend = 0;
		List<Long> plusY = new ArrayList<Long>();
		List<Long> minusY = new ArrayList<Long>();
		for (long y : reasonableY) {
			if (y > predictBase) {
				trend += 1;
				plusY.add(y);
			}
			if (y < predictBase) {
				trend -= 1;
				minusY.add(y);
			}
		}

		long predictY;
		if (trend == 0) {
			predictY = predictBase;
		} else if (trend > 0) {
			predictY = Statistics.getAverage(plusY);
		} else {
			predictY = Statistics.getAverage(minusY);
		}

//		System.out.println(offset * 1.0 / predictBase);
//		System.out.println(predictBase + " " + offset + " " + predictY);
		return predictY;

	}

	// 加权平均
	public static List<Long> weightSmooth(List<Long> Y) {
		int size = Y.size();

		List<Long> smoothedY = new ArrayList<Long>();
		for (int i = 0; i < size; ++i)
			smoothedY.add(0L);

		double[] weight = { 0.07, 0.13, 0.18, 0.24, 0.18, 0.13, 0.07 };

		int half_period = 3;

		for (int i = 0; i < size; ++i) {

			int i_start = i - half_period;
			i_start = Math.max(0, i_start);

			int i_end = i + half_period + 1;
			i_end = Math.min(size, i_end);

			if (i_end - i_start < 7) {
				smoothedY.set(i, Y.get(i));
			} else {
				double sum = 0;
				int index = 0;
				for (int j = i_start; j < i_end; ++j) {
					sum += Y.get(j) * weight[index];
					index++;
				}
				smoothedY.set(i, (long) sum);
			}
		}
		return smoothedY;
	}

	// 加权平均
	public static List<Long> weightSmooth2(List<Long> Y) {
		int size = Y.size();

		List<Long> smoothedY = new ArrayList<Long>();
		for (int i = 0; i < size; ++i)
			smoothedY.add(0L);

		double[] weight = { 0.07, 0.13, 0.18, 0.24, 0.18, 0.13, 0.07 };

		int half_period = 3;

		for (int i = 0; i < size; ++i) {

			int i_start = i - half_period;
			i_start = Math.max(0, i_start);

			int i_end = i + half_period + 1;
			i_end = Math.min(size, i_end);

			if (i_end - i_start < 7) {
				double sum = 0;
				int num = 0;
				for (int j = i_start; j < i_end; ++j) {
					sum += Y.get(j);
					num++;
				}
				smoothedY.set(i, (long) (sum / num));
			} else {
				double sum = 0;
				int index = 0;
				for (int j = i_start; j < i_end; ++j) {
					sum += Y.get(j) * weight[index];
					index++;
				}
				smoothedY.set(i, (long) sum);
			}
		}
		return smoothedY;
	}

	
	/** 指数平滑 */
	public static List<Long> exponentialSmooth(List<Long> Y,double rate){
		List<Long> smoothedY = new ArrayList<Long>();
		double lastY = Y.get(0);
		
		for (int i = 0; i < Y.size(); ++i){
			lastY = Y.get(i)*rate+lastY*(1-rate);
			smoothedY.add((long)lastY);
		}
		return smoothedY;
	}
}
