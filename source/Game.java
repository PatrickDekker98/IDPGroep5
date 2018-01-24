import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.JPanel;
import javax.swing.Timer;

import jaco.mp3.player.MP3Player;

@SuppressWarnings("serial")
public class Game extends JPanel implements KeyListener {

	private static final int ENTITEIT_GROOTTE = 10;

	private int etenX, etenY, ballen;
	private int score = 0;

	private boolean in_game = true;
	private boolean geluidAfgespeeld;

	private boolean[] richtingen = new boolean[4];
	private final int x[] = new int[900];
	private final int y[] = new int[900];

	private Image hoofd;
	private Image bal;
	private Image eten;
	private Image achtergrond;

	private Timer timer;

	private static final Dimension DIMENSIES = new Dimension(300, 300);

	public Game() throws IOException {
		timer = new Timer(50, new TimerListener());
		timer.start();
		addKeyListener(this);
		setBackground(Color.BLACK);
		setFocusable(true);
		setPreferredSize(DIMENSIES);
		laadAfbeeldingen();
		initieerGame();
	}

	private void initieerGame() {
		ballen = 3;
		for (int z = 0; z < ballen; z++) {
			x[z] = 50 - z * ENTITEIT_GROOTTE;
			y[z] = 50;
		}
		plaatsEten();
	}

	private void laadAfbeeldingen() throws IOException {
		bal = ImageIO.read(new File("data/images/bal.png"));
		hoofd = ImageIO.read(new File("data/images/hoofd.png"));
		eten = ImageIO.read(new File("data/images/eten.png"));
		achtergrond = ImageIO.read(new File("data/images/achtergrond.png"));
	}

	private void beweegEntiteit() {
		for (int z = ballen; z > 0; z--) {
			x[z] = x[(z - 1)];
			y[z] = y[(z - 1)];
		}
		setDirection();
		if (richtingen[0])
			y[0] -= ENTITEIT_GROOTTE;
		else if (richtingen[1])
			y[0] += ENTITEIT_GROOTTE;
		else if (richtingen[2])
			x[0] += ENTITEIT_GROOTTE;
		else if (richtingen[3])
			x[0] -= ENTITEIT_GROOTTE;
	}

	private void tekenScore(Graphics g) {
		String text = "Score: " + score;
		Font font = new Font("Helvetica", Font.BOLD, 14);
		g.setColor(Color.CYAN);
		g.setFont(font);
		g.drawString(text, 225, 20);
	}

	private void tekenEntiteiten(Graphics g) {
		g.drawImage(eten, etenX, etenY, this);
		for (int index = 0; index < ballen; index++) {
			if (index == 0)
				g.drawImage(hoofd, x[index], y[index], this);
			else
				g.drawImage(bal, x[index], y[index], this);
		}
		if (!in_game) {
			g.drawImage(achtergrond, 0, 0, this);
			if (!geluidAfgespeeld) {
				speelGeluidAf("data/sounds/gameover.mp3");
				geluidAfgespeeld = true;
			}
		}
	}

	private void plaatsEten() {
		int random = (int) (Math.random() * 29);
		etenX = (random * ENTITEIT_GROOTTE);
		random = (int) (Math.random() * 29);
		etenY = (random * ENTITEIT_GROOTTE);
	}

	private void verwerkenEten() {
		if (x[0] == etenX && y[0] == etenY) {
			score += 5;
			ballen++;
			plaatsEten();
			speelGeluidAf("data/sounds/eten.mp3");
		}
	}

	private void checkBotsingen() {
		for (int z = ballen; z > 0; z--) {
			if ((z > 4) && (x[0] == x[z]) && (y[0] == y[z])) {
				in_game = false;
				timer.stop();
			}
		}
		if (y[0] >= 300)
			y[0] = 0;
		else if (y[0] < 0)
			y[0] = 300;
		else if (x[0] >= 300)
			x[0] = 0;
		else if (x[0] < 0)
			x[0] = 300;
	}

	private void speelGeluidAf(String pad) {
		new MP3Player(new File(pad)).play();
	}

	private void setDirection() {
		final int x = SocketServer.DIRECTIONS[0];
		final int y = SocketServer.DIRECTIONS[1];
		if (x >= 1 && y == -1) {
			richtingen[0] = true;
			richtingen[1] = false;
			richtingen[2] = false;
			richtingen[3] = false;
		} else if (x >= 1 && y == 1) {
			richtingen[1] = true;
			richtingen[0] = false;
			richtingen[1] = false;
			richtingen[2] = false;
		} else if (x == 1 && y == 0) {
			richtingen[2] = true;
			richtingen[0] = false;
			richtingen[1] = false;
			richtingen[3] = false;
		} else if (x == -1 && y == 0) {
			richtingen[3] = true;
			richtingen[0] = false;
			richtingen[1] = false;
			richtingen[2] = false;
		}
	}

	@Override
	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		tekenEntiteiten(g);
		tekenScore(g);
	}

	@Override
	public void keyPressed(KeyEvent arg0) {
		switch (arg0.getKeyCode()) {
		case KeyEvent.VK_DOWN:
			if (!richtingen[0]) {
				richtingen[1] = true;
				richtingen[2] = false;
				richtingen[3] = false;
			}
			break;
		case KeyEvent.VK_UP:
			if (!richtingen[1]) {
				richtingen[0] = true;
				richtingen[2] = false;
				richtingen[3] = false;
			}
			break;
		case KeyEvent.VK_LEFT:
			if (!richtingen[2]) {
				richtingen[0] = false;
				richtingen[1] = false;
				richtingen[3] = true;
			}
			break;
		case KeyEvent.VK_RIGHT:
			if (!richtingen[3]) {
				richtingen[0] = false;
				richtingen[1] = false;
				richtingen[2] = true;
			}
			break;
		}
		repaint();
	}

	@Override
	public void keyReleased(KeyEvent arg0) {
		// TODO Auto-generated method stub
	}

	@Override
	public void keyTyped(KeyEvent arg0) {
		// TODO Auto-generated method stub
	}

	private class TimerListener implements ActionListener {

		@Override
		public void actionPerformed(ActionEvent e) {
			if (in_game) {
				verwerkenEten();
				checkBotsingen();
				beweegEntiteit();
			}
			repaint();
		}
	}

}
