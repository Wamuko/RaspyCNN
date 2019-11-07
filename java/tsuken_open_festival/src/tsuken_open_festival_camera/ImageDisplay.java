package tsuken_open_festival_camera;

import java.awt.Dimension;
import java.awt.Font;
import java.net.MalformedURLException;
import java.net.URL;

import javax.swing.BoxLayout;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;


public class ImageDisplay implements Runnable
{
	private JLabel l1, l2;;
	private JFrame jf;
	private Thread th;

	public void run()
	{
		while (true)
		{
			try
			{
				Thread.sleep(1000);
			}
			catch (InterruptedException e)
			{
				e.printStackTrace();
			}
		}
	}

	public ImageDisplay()
	{
		jf = new JFrame("Image Display");

		JPanel p = new JPanel();
		jf.add(p);

		p.setLayout(new BoxLayout(p, BoxLayout.PAGE_AXIS));

		l1 = new JLabel("Camera");
		l1.setFont(new Font("Arial", Font.PLAIN, 30));
		l1.setPreferredSize(new Dimension(600,100));

		l2 = new JLabel();
		l2.setPreferredSize(new Dimension(600,450));

		p.add(l1);
		p.add(l2);

		jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		jf.pack();
		jf.setVisible(true);

		th = new Thread(this);
		th.start();
	}

	public void show(URL u)
	{
		l2.setIcon(new ImageIcon(u));
	}

	public static void main(String[] args)
	{
		ImageDisplay id1 = new ImageDisplay();
		ImageDisplay id2 = new ImageDisplay();

		try
		{
			URL u1 = new URL("file:d:/camera_1.JPG");
			id1.show(u1);
		}
		catch (MalformedURLException e)
		{
			e.printStackTrace();
		}

		try
		{
			URL u2 = new URL("file:d:/camera_1.JPG");
			id2.show(u2);
		}
		catch (MalformedURLException e)
		{
			e.printStackTrace();
		}
	}

}
