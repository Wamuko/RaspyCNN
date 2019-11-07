package tsuken_open_festival_camera;

import java.awt.Component;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

class ReadImageComponent extends Component implements Runnable
{
	private long preLastModified, nowLastModified;
	private String filePath = null;

	BufferedImage img = null;
	BufferedImage newimg = null;

	int width = 100;
	int height = 100;

	int x, y, neww, newh, color;

	private Thread thread;

//	ReadImageComponent(String date, String filename)
	ReadImageComponent(String filename)
	{
//		filePath = "z://nict/mobileNet/saved_images/" + date + "/" + filename + ".jpg";
		filePath = "z://nict/mobileNet/saved_images/" + filename + ".jpg";
//		filePath = "d:/" + filename + ".JPG";

		thread = new Thread(this);
		thread.start();

		try
		{
			img = ImageIO.read(new File(filePath));
		}
		catch (IOException e)
		{
			System.out.println("image file not found. [" + filePath + "]");
		}

		if (img != null)
		{
			width = img.getWidth(null);
			height = img.getHeight(null);
		}

		// 新しい画像サイズを計算
		neww = width * 2;
		newh = height * 2;

// 新しい画像を作成
// ２４ビットカラーの画像を作成
		try
		{
			newimg = new BufferedImage(neww, newh, BufferedImage.TYPE_INT_RGB);
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}

// 処理本体
		for (y = 0; y < height; ++y)
		{
			for (x = 0; x < width; ++x)
			{
// (x,y)の色を取得
				color = img.getRGB(x, y);

// ２ｘ２の４倍に拡大
				newimg.setRGB(x * 2, y * 2, color);
				newimg.setRGB(x * 2 + 1, y * 2, color);
				newimg.setRGB(x * 2, y * 2 + 1, color);
				newimg.setRGB(x * 2 + 1, y * 2 + 1, color);
			}
		}
	}

	public void paint(Graphics graphics)
	{
		graphics.drawImage(newimg, 0, 0, null);
	}

	public Dimension getPreferredSize()
	{
		if (newimg == null)
		{
			width = 100;
			height = 100;
		}

		return new Dimension(neww, newh);
	}

	public void run()
	{
		File f = new File(filePath);

		while (true)
		{
			preLastModified = f.lastModified();

			try
			{
				Thread.sleep(1000);
			}
			catch (InterruptedException e)
			{
				System.out.println("error 1");
			}

			nowLastModified = f.lastModified();

			if (preLastModified != nowLastModified)
			{
				try
				{
					img = ImageIO.read(new File(filePath));

					if (img != null)
					{
						width = img.getWidth(null);
						height = img.getHeight(null);
					}

					// 新しい画像サイズを計算
					neww = width * 2;
					newh = height * 2;

					// 新しい画像を作成
					// ２４ビットカラーの画像を作成
					try
					{
						newimg = new BufferedImage(neww, newh, BufferedImage.TYPE_INT_RGB);
					}
					catch (Exception e)
					{
						e.printStackTrace();
					}

					// 処理本体
					for (y = 0; y < height; ++y)
					{
						for (x = 0; x < width; ++x)
						{
							// (x,y)の色を取得
							color = img.getRGB(x, y);

							// ２ｘ２の４倍に拡大
							newimg.setRGB(x * 2, y * 2, color);
							newimg.setRGB(x * 2 + 1, y * 2, color);
							newimg.setRGB(x * 2, y * 2 + 1, color);
							newimg.setRGB(x * 2 + 1, y * 2 + 1, color);
						}
					}

					repaint();
					System.out.println("Reload file.");
				}
				catch (IOException e)
				{
					System.out.println("image file not found. [" + filePath + "]");
				}
			}
		}
	}
}

//package tsuken_open_festival_camera;
//
//import java.awt.Component;
//import java.awt.Dimension;
//import java.awt.Graphics;
//import java.awt.image.BufferedImage;
//import java.io.File;
//import java.io.IOException;
//
//import javax.imageio.ImageIO;
//
//class ReadImageComponent extends Component implements Runnable
//{
//	private long preLastModified, nowLastModified;
//	private String filePath = null;
//
//	BufferedImage img = null;
//	BufferedImage newimg = null;
//
//	int width = 100;
//	int height = 100;
//
//	int x, y, neww, newh, color;
//
//	private Thread thread;
//
////	ReadImageComponent(String date, String filename)
//	ReadImageComponent(String filename)
//	{
////		filePath = "z://nict/mobileNet/saved_images/" + date + "/" + filename + ".jpg";
//		filePath = "z://nict/mobileNet/saved_images/" + filename + ".jpg";
////		filePath = "d:/" + filename + ".JPG";
//
//		thread = new Thread(this);
//		thread.start();
//
//		try
//		{
//			img = ImageIO.read(new File(filePath));
//		}
//		catch (IOException e)
//		{
//			System.out.println("image file not found. [" + filePath + "]");
//		}
//
//		if (img != null)
//		{
//			width = img.getWidth(null);
//			height = img.getHeight(null);
//		}
//
//		// 新しい画像サイズを計算
//		neww = width * 2;
//		newh = height * 2;
//
//// 新しい画像を作成
//// ２４ビットカラーの画像を作成
//		try
//		{
//			newimg = new BufferedImage(neww, newh, BufferedImage.TYPE_INT_RGB);
//		}
//		catch (Exception e)
//		{
//			e.printStackTrace();
//		}
//
//// 処理本体
//		for (y = 0; y < height; ++y)
//		{
//			for (x = 0; x < width; ++x)
//			{
//// (x,y)の色を取得
//				color = img.getRGB(x, y);
//
//// ２ｘ２の４倍に拡大
//				newimg.setRGB(x * 2, y * 2, color);
//				newimg.setRGB(x * 2 + 1, y * 2, color);
//				newimg.setRGB(x * 2, y * 2 + 1, color);
//				newimg.setRGB(x * 2 + 1, y * 2 + 1, color);
//			}
//		}
//	}
//
//	public void paint(Graphics graphics)
//	{
//		graphics.drawImage(newimg, 0, 0, null);
//	}
//
//	public Dimension getPreferredSize()
//	{
//		if (newimg == null)
//		{
//			width = 100;
//			height = 100;
//		}
//
//		return new Dimension(neww, newh);
//	}
//
//	public void run()
//	{
//		File f = new File(filePath);
//
//		while (true)
//		{
//			preLastModified = f.lastModified();
//
//			try
//			{
//				Thread.sleep(1000);
//			}
//			catch (InterruptedException e)
//			{
//				System.out.println("error 1");
//			}
//
//			nowLastModified = f.lastModified();
//
//			if (preLastModified != nowLastModified)
//			{
//				try
//				{
//					img = ImageIO.read(new File(filePath));
//
//					if (img != null)
//					{
//						width = img.getWidth(null);
//						height = img.getHeight(null);
//					}
//
//					// 新しい画像サイズを計算
//					neww = width * 2;
//					newh = height * 2;
//
//					// 新しい画像を作成
//					// ２４ビットカラーの画像を作成
//					try
//					{
//						newimg = new BufferedImage(neww, newh, BufferedImage.TYPE_INT_RGB);
//					}
//					catch (Exception e)
//					{
//						e.printStackTrace();
//					}
//
//					// 処理本体
//					for (y = 0; y < height; ++y)
//					{
//						for (x = 0; x < width; ++x)
//						{
//							// (x,y)の色を取得
//							color = img.getRGB(x, y);
//
//							// ２ｘ２の４倍に拡大
//							newimg.setRGB(x * 2, y * 2, color);
//							newimg.setRGB(x * 2 + 1, y * 2, color);
//							newimg.setRGB(x * 2, y * 2 + 1, color);
//							newimg.setRGB(x * 2 + 1, y * 2 + 1, color);
//						}
//					}
//
//					repaint();
//					System.out.println("Reload file.");
//				}
//				catch (IOException e)
//				{
//					System.out.println("image file not found. [" + filePath + "]");
//				}
//			}
//		}
//	}
//}
//}