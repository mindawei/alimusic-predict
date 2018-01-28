

import java.math.BigDecimal;
import jamlab.Polyfit;
import jamlab.Polyval;

public class Fitting{
	
	/**
	 * @Title: getNextY 返回下一个值
	 * @param order 多项式拟合的最高次数
	 * @param x x变量
	 * @param y y值
	 * @param nextX 下一个要预测的值的x变量 
	 * @return
	 * double  拟合值
	 */
	public static double getNextY(int order ,double[] x,double[] y,double nextX){
		  Polyfit polyfit = null;
		  Polyval polyval;
		   try {
		        //创建多项式拟合对象，其中的4表示是4次多项式拟合
		        polyfit = new Polyfit(x, y, order);
		        polyval = new Polyval(new double[]{nextX}, polyfit);
		        BigDecimal bd = new BigDecimal(polyval.getYout()[0]).setScale(2, BigDecimal.ROUND_HALF_UP);
		        return Double.parseDouble(bd.toString());
		    }catch (Exception e) {
		        System.out.println("Error : " + e.getMessage() + "\n");
		        e.printStackTrace();
		        System.exit(0);
		    }
		   return 0;
	}
	
	public static void main(String[] args) {
	    //X轴
	    //  double[] x = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 };
	    //Y轴
	    // double[] y = { 2.3, 2.3, 2.4, 2.8, 2.9, 2.6, 2.9, 3.2, 3.9, 4.0, 4.3, 4.2, 4.2, 4.0, 3.8, 4.0, 3.5, 3.3, 3.2, 2.8 };
	  
	    double[] x = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
	    double[] y = { 2, 4, 6, 8, 10, 12, 14, 16, 18, 20.2};
	    int order = 1;
	    System.out.println(getNextY(order, x, y, 10));
	}
}
