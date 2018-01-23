import java.awt.EventQueue;
import java.io.IOException;

import javax.swing.JFrame;

@SuppressWarnings("serial")
public class Snake extends JFrame {

	public Snake() throws IOException {
		add(new Game());
		setResizable(false);
		pack();
		setTitle("Snake - IDP");
		setLocationRelativeTo(null);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			@Override
			public void run() {
				JFrame ex = null;
				try {
					ex = new Snake();
				} catch (IOException e) {
					e.printStackTrace();
				}
				ex.setVisible(true);
			}
		});
	}
}