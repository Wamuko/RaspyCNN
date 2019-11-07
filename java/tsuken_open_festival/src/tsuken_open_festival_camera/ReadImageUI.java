package tsuken_open_festival_camera;

import java.awt.BorderLayout;
import java.awt.Container;
import java.awt.Font;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;
import javax.swing.JLabel;

class ReadImageUI extends JFrame
{
	ReadImageComponent component = null;

//	ReadImageUI(String cameraName, String date, String filename)
	ReadImageUI(String cameraName, String filename)
	{
		setTitle("IoT技術応用カメラ 展示テスト");
		setSize(320, 160);
		setLayout(new BorderLayout());
		Container contentPane = getContentPane();
//		component = new ReadImageComponent(date, filename);
		component = new ReadImageComponent(filename);
		contentPane.add(component, BorderLayout.CENTER);
		JLabel cameraLabel = new JLabel(cameraName);
		cameraLabel.setFont(new Font("Serif", Font.ITALIC, 30));
		contentPane.add(cameraLabel, BorderLayout.NORTH);
	}

	public static void main(String[] args)
	{
//		String date = args[0];

		String cameraName, filename;

		cameraName = "camera_1";
		filename = "172.16.203.1";
//		filename = "camera_1";
//		ReadImageUI readImageUI1 = new ReadImageUI(cameraName, date, filename);
		ReadImageUI readImageUI1 = new ReadImageUI(cameraName, filename);

		cameraName = "camera_2";
		filename = "172.16.204.1";
//		filename = "camera_2";
//		ReadImageUI readImageUI2 = new ReadImageUI(cameraName, date, filename);
		ReadImageUI readImageUI2 = new ReadImageUI(cameraName, filename);

		WindowAdapter windowAdapter = new WindowAdapter()
		{
			public void windowClosing(WindowEvent e)
			{
				System.exit(0);
			}
		};

		readImageUI1.addWindowListener(windowAdapter);
		readImageUI1.pack();
		readImageUI1.setVisible(true);

		readImageUI2.addWindowListener(windowAdapter);
		readImageUI2.pack();
		readImageUI2.setVisible(true);
	}
}

//package tsuken_open_festival_camera;
//
//import java.awt.BorderLayout;
//import java.awt.Container;
//import java.awt.Font;
//import java.awt.event.WindowAdapter;
//import java.awt.event.WindowEvent;
//
//import javax.swing.JFrame;
//import javax.swing.JLabel;
//
//class ReadImageUI extends JFrame
//{
//	ReadImageComponent component = null;
//
////	ReadImageUI(String cameraName, String date, String filename)
//	ReadImageUI(String cameraName, String filename)
//	{
//		setTitle("IoT技術応用カメラ 展示テスト");
//		setSize(320, 160);
//		setLayout(new BorderLayout());
//		Container contentPane = getContentPane();
////		component = new ReadImageComponent(date, filename);
//		component = new ReadImageComponent(filename);
//		contentPane.add(component, BorderLayout.CENTER);
//		JLabel cameraLabel = new JLabel(cameraName);
//		cameraLabel.setFont(new Font("Serif", Font.ITALIC, 30));
//		contentPane.add(cameraLabel, BorderLayout.NORTH);
//	}
//
//	public static void main(String[] args)
//	{
////		String date = args[0];
//
//		String cameraName, filename;
//
//		cameraName = "camera_1";
//		filename = "172.16.203.1";
////		filename = "camera_1";
////		ReadImageUI readImageUI1 = new ReadImageUI(cameraName, date, filename);
//		ReadImageUI readImageUI1 = new ReadImageUI(cameraName, filename);
//
//		cameraName = "camera_2";
//		filename = "172.16.204.1";
////		filename = "camera_2";
////		ReadImageUI readImageUI2 = new ReadImageUI(cameraName, date, filename);
//		ReadImageUI readImageUI2 = new ReadImageUI(cameraName, filename);
//
//		WindowAdapter windowAdapter = new WindowAdapter()
//		{
//			public void windowClosing(WindowEvent e)
//			{
//				System.exit(0);
//			}
//		};
//
//		readImageUI1.addWindowListener(windowAdapter);
//		readImageUI1.pack();
//		readImageUI1.setVisible(true);
//
//		readImageUI2.addWindowListener(windowAdapter);
//		readImageUI2.pack();
//		readImageUI2.setVisible(true);
//	}
//}