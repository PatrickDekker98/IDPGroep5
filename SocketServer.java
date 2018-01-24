import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class SocketServer {
	
	private static final int PORT = 12345;
	
	public static void main(String args[]) throws IOException {
		ServerSocket server = new ServerSocket(PORT);
		System.out.println("Server is waiting for a response of a client on port " + PORT + ".");
		while (true) {
			Socket connected = server.accept();
			System.out.println("Connected with client: " + connected.getInetAddress() + ":" + connected.getPort());
			BufferedReader in = new BufferedReader(new InputStreamReader(connected.getInputStream()));
			String line;
			while ((line = in.readLine()) != null) {
				System.out.println(line);
			}
		}
	}
}