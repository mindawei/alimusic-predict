package arima;

import java.util.ArrayList;
import java.util.List;


public class ARIMAiFlex {

	private int[][] modelOri = new int[][] { { 0, 1 }, { 1, 0 }, { 1, 1 }, { 0, 2 },
			{ 2, 0 }, { 2, 2 }, { 1, 2 }, { 2, 1 }, { 3, 0 }, { 0, 3 },
			{ 3, 1 }, { 1, 3 }, { 3, 2 }, { 2, 3 }, { 3, 3 } };

	private Modelandpara mp = null;
	private double[][] predictErr = new double[7][modelOri.length];
	private double[] traindataArray = null;
	private double validate = 0; // 验证值
	private double[] predataArray = null;

	double[] dataArrayPredict = null;
	
	private int memory = 60;// 训练的时候预测的值的个数

	public ARIMAiFlex() {}
	
	public Long predict(List<Long> Y){
		
			
		double[] dataArray =new double[Y.size()]; 
		for(int j=0;j<dataArray.length;j++){
			dataArray[j]=Y.get(j);
		}
		
		// 模型训练
		int[] parameter = this.Train(dataArray);
		// 预测数据初始化
		return (long) Predict(dataArray, memory, parameter);
		
	}

	public void preData(double[] dataArray, int type, int memory) {
		this.traindataArray = new double[dataArray.length - memory];
		System.arraycopy(dataArray, type, traindataArray, 0,
				traindataArray.length);
		this.validate = dataArray[traindataArray.length + type];// 最后一个值作为训练时候的验证值。

	}

	public int Predict(double[] dataArray, int memory, int[] parameter) {
		
		this.predataArray = new double[dataArray.length - memory];
		System.arraycopy(dataArray, memory, predataArray, 0,
				predataArray.length);

		ARIMA arima = new ARIMA(predataArray, parameter[0]); // 对原始数据做几阶差分处理0,1,2,7

		mp = arima.getARIMAmodel(modelOri[parameter[1]]);
		return arima.aftDeal(arima.predictValue(mp.model[0], mp.model[1],
				mp.para));

	}

	/** 训练获得较好的参数 */
	public int[] Train(double[] dataArray) {

		for (int datai = 0; datai < memory; datai++) {

			this.preData(dataArray, datai, memory);// 准备训练数据

			for (int diedai = 0; diedai < 7; diedai++) {
				ARIMA arima = new ARIMA(traindataArray, diedai); // 对原始数据做几阶差分处理0,1,2,7

				// 统计每种模型的预测平均值
				for (int modeli = 0; modeli < modelOri.length; modeli++) {
					mp = arima.getARIMAmodel(modelOri[modeli]);
					int val = arima.aftDeal(arima.predictValue(mp.model[0],
							mp.model[1], mp.para));
					int predictValuetemp = val;
					// 计算训练误差
					predictErr[diedai][modeli] += Math.abs(100
							* (predictValuetemp - validate) / validate);
				}
			}
		}

		double minvalue = Double.MAX_VALUE;
		int tempi = 0;
		int tempj = 0;

		// 找到最好的1个
		for (int i = 0; i < predictErr.length; i++) {
			for (int j = 0; j < predictErr[i].length; j++) {
				if (predictErr[i][j] < minvalue) {
					minvalue = predictErr[i][j];
					tempi = i;
					tempj = j;
				}
			}
		}
//		System.out.println(tempi+" "+tempj);
		return new int[] { tempi, tempj };
	}

}
