package arima;
import Jama.Matrix;
import Jama.SingularValueDecomposition;

public class Test {
	public static void main(String[] args) {
		System.out.println("HelloWorld");
		
		double[][] array = { { 1., 2.,3. }, {4, 2., 3. },{9, 5., 7. } };
		
		System.out.println(array.length);
		Matrix A = new Matrix(array);
		
		
		A.inverse().print(8, 8);
		pinv(A).print(8, 8);

	}
	
	/** 伪逆矩阵 */
	private static Matrix pinv(Matrix A){
		SingularValueDecomposition svd =A.svd();
		Matrix S = svd.getS();
		Matrix V = svd.getV().transpose();
		Matrix U = svd.getU();
		//将S中非0元素取倒数
		Matrix sinv = UnaryNotZeroElement(S);
		Matrix inv = V.times(sinv).times(U.transpose());
		return inv;
	}
	
	//将矩阵中非0元素取倒数
	private static Matrix UnaryNotZeroElement(Matrix x) {
		double[][] array=x.getArray();
		for(int i=0;i<array.length;i++){
			for(int j=0;j<array[i].length;j++){
				if(array[i][j]!=0){
					array[i][j]=1.0/array[i][j];
				}
			}
		}
		return new Matrix(array);
	}

}
