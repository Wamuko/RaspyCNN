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
	private String s = ReadImageUI.cameraName;
	private String filePath = "d:/" + s + ".JPG";

	BufferedImage bufferedImage = null;

	private Thread thread;

	ReadImageComponent()
	{

		thread = new Thread(this);
		thread.start();

		try
		{
			bufferedImage = ImageIO.read(new File(filePath));
		}
		catch (IOException e)
		{
			System.out.println("image file not found. [" + filePath + "]");
		}
	}

	public void paint(Graphics graphics)
	{
		graphics.drawImage(bufferedImage, 0, 0, null);
	}

	public Dimension getPreferredSize()
	{
		int width = 100;
		int height = 100;
		if (bufferedImage != null)
		{// [125]
			width = bufferedImage.getWidth(null);
			height = bufferedImage.getHeight(null);
		}
		return new Dimension(width, height);
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
					bufferedImage = ImageIO.read(new File(filePath));
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
//{// [100]
//	private long preLastModified, nowLastModified;
//	private String filePath = "d:/image.JPG";
//
//	BufferedImage bufferedImage = null;// [101]
//
//	private Thread thread;
//
//	ReadImageComponent()
//	{// [102]
//
//		thread = new Thread(this);
//		thread.start();
//
//		try
//		{// [104]
//			bufferedImage = ImageIO.read(new File(filePath));// [105]
//		}
//		catch (IOException e)
//		{// [106]
//			System.out.println("image file not found. [" + filePath + "]");// [107]
//		}
//	}
//
//	public void paint(Graphics graphics)
//	{// [110]
//		graphics.drawImage(bufferedImage, 0, 0, null);// [111]
//	}
//
//	public Dimension getPreferredSize()
//	{// [120]
//		int width = 100;// [123]
//		int height = 100;// [134]
//		if (bufferedImage != null)
//		{// [125]
//			width = bufferedImage.getWidth(null);// [126]
//			height = bufferedImage.getHeight(null);// [127]
//		}
//		return new Dimension(width, height);// [128]
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
//				System.out.println("なんかスレッド上手く走らんわ");
//			}
//
//			nowLastModified = f.lastModified();
//
//			if (preLastModified != nowLastModified)
//			{
//				System.out.println("画像変わったで");
//
//				try
//				{// [104]
//					bufferedImage = ImageIO.read(new File(filePath));// [105]
//					repaint();
//				}
//				catch (IOException e)
//				{// [106]
//					System.out.println("image file not found. [" + filePath + "]");// [107]
//				}
//			}
//		}
//	}
//}
//
