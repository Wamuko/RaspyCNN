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
	public static String cameraName;

	ReadImageUI(String cameraName)
	{
		setTitle("IoT技術応用カメラ 展示テスト");
		setSize(320, 160);
		setLayout(new BorderLayout());
		Container contentPane = getContentPane();
		component = new ReadImageComponent();
		contentPane.add(component, BorderLayout.CENTER);
		JLabel cameraLabel = new JLabel(cameraName);
		cameraLabel.setFont(new Font("Serif", Font.ITALIC, 30));
		contentPane.add(cameraLabel, BorderLayout.NORTH);
	}

	public static void main(String[] args)
	{
		cameraName = "camera_1";
		ReadImageUI readImageUI1 = new ReadImageUI(cameraName);

		cameraName = "camera_2";
		ReadImageUI readImageUI2 = new ReadImageUI(cameraName);

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

// package tsuken_open_festival_camera;
//
// import java.awt.BorderLayout;
// import java.awt.Container;
// import java.awt.Font;
// import java.awt.event.WindowAdapter;
// import java.awt.event.WindowEvent;
//
// import javax.swing.JFrame;
// import javax.swing.JLabel;
//
// class ReadImageUI extends JFrame
// {// [1]
// ReadImageComponent component = null;// [2]
//
// ReadImageUI()
// {// [3]
// setTitle("IoT技術応用カメラ 展示テスト");// [4]
// setSize(320, 160);// [5]
// setLayout(new BorderLayout());// [6]
// Container contentPane = getContentPane();// [7]
// component = new ReadImageComponent();// [8]
// contentPane.add(component, BorderLayout.CENTER);// [9]
// JLabel cameraLabel = new JLabel("camera 1");// [10]
// cameraLabel.setFont(new Font("Serif", Font.ITALIC, 30));
// contentPane.add(cameraLabel, BorderLayout.NORTH);// [12]
// }
//
// public static void main(String[] args)
// {// [30]
// ReadImageUI readImageUI = new ReadImageUI();// [31]
// WindowAdapter windowAdapter = new WindowAdapter()
// {
// public void windowClosing(WindowEvent e)
// {
// System.exit(0);
// }
// };// [32]
// readImageUI.addWindowListener(windowAdapter);// [33]
// readImageUI.pack();// [34]
// readImageUI.setVisible(true);// [35]
// }
// }
