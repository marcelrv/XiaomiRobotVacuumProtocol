package RRMap;

import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Stroke;
import java.awt.BasicStroke;

import java.awt.geom.Line2D;
import java.awt.geom.Ellipse2D;
import java.awt.RenderingHints;
import java.awt.Transparency;
import java.awt.color.ColorSpace;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.geom.AffineTransform;
import java.awt.image.AffineTransformOp;
import java.awt.image.BufferedImage;
import java.awt.image.ColorModel;
import java.awt.image.ComponentColorModel;
import java.awt.image.DataBuffer;
import java.awt.image.DataBufferByte;
import java.awt.image.Raster;
import java.awt.image.SampleModel;
import java.awt.image.WritableRaster;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.zip.GZIPInputStream;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;

public class RRDraw extends JFrame {

    /**
    *
    */
    private static final long serialVersionUID = 2623447051590306992L;
    JFrame parent;
    RRDrawPanel rrDrawPanel;

    public RRDraw() {
        super("RR Map Viewer");
        setSize(350, 400);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        parent = this;
        rrDrawPanel = new RRDrawPanel();
        Container c = getContentPane();
        // The default BorderLayout will work better.
        // c.setLayout(new FlowLayout());

        JButton openButton = new JButton("Open");
        final JLabel statusbar = new JLabel("Output of your selection will go here");

      //  File file = new File("C:\\temp\\map\\roboroommap7.gz");
      //  RRFileParser loadImage = loadImage(file);
      //  statusbar.setText(file.getName() + " size " + loadImage.getImgWidth() + "x" + loadImage.getImgHeight());
      //  rrDrawPanel.setSize(loadImage.getImgWidth(), loadImage.getImgHeight());

        openButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent ae) {
                JFileChooser chooser = new JFileChooser("images");

                int option = chooser.showOpenDialog(parent);
                if (option == JFileChooser.APPROVE_OPTION) {
                    File file = chooser.getSelectedFile();
                    RRFileParser loadImage = loadImage(file);
                    statusbar.setText(file.getName() + " size " + loadImage.getImgWidth() + "x" + loadImage.getImgHeight());
                    rrDrawPanel.setSize(loadImage.getImgWidth(), loadImage.getImgHeight());
            
                } else {
                    statusbar.setText("You cancelled.");
                }
            }
        });

        JPanel north = new JPanel();
        north.add(openButton);
        north.add(statusbar);

        north.setBackground(Color.GRAY);
        north.setForeground(Color.BLUE);
        c.add(north, "First");

        c.add(new JScrollPane(rrDrawPanel), "Center");

    }

    /**
     * load Gzipped RR file
     */
    private RRFileParser loadImage(File file) {

        try {
            byte[] inputdata = readGZFile(file);
            RRFileParser rf = new RRFileParser(inputdata);
            System.out.println(rf.toSting());
            int l = (int) rf.getImgHeight();
            int w = (int) rf.getImgWidth();
            byte[] buffer = rf.getImage();
            rrDrawPanel.setRRFileDecoder(rf);

            setSize(w, l);
            return rf;
        } catch (IOException e) {
            System.out.println("read error: " + e.getMessage());
        }
        return null;
    }

    public static void main(String args[]) {
        System.setProperty("swing.defaultlaf", "javax.swing.plaf.metal.MetalLookAndFeel");
        RRDraw vc = new RRDraw();
        vc.setVisible(true);
    }

    public byte[] readGZFile(File file) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try (GZIPInputStream in = new GZIPInputStream(new FileInputStream(file))) {
            int bufsize = 1024;
            byte[] buf = new byte[bufsize];
            int readbytes = 0;
            readbytes = in.read(buf);
            while (readbytes != -1) {
                baos.write(buf, 0, readbytes);
                readbytes = in.read(buf);
            }
            baos.flush();
            return baos.toByteArray();
        } catch (IOException e) {
            e.printStackTrace();
            throw e;
        }
    }

}

class RRDrawPanel extends JPanel {
    /**
     *
     */
    private static final long serialVersionUID = 8791558011928073284L;
    BufferedImage image;
    Dimension size = new Dimension();
    private RRFileParser rf;

    public RRDrawPanel() {
    }

    public void setRRFileDecoder(RRFileParser rf) {
        this.rf = rf;
    }

    void drawMap(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;
        if (rf != null) {

            int z = 0;
            for (int y = 0; y < rf.getImgHeight() - 1; y++) {
                for (int x = 0; x < rf.getImgWidth() - 1; x++) {

                    // int type = rf.getImage()[x] ;
                    switch (rf.getImage()[x + rf.getImgWidth() * y]) {
                    case 0x00:
                        g2d.setColor(new Color(19, 87, 148));
                        break;
                    case 0x01:
                        g2d.setColor(new Color(100, 196, 254));
                        break;
                    default:
                        g2d.setColor(new Color(32, 115, 185));

                        break;
                    }
                    float Xpos = (float) 1024 - (x + rf.getLeft()) - rf.getLeft();
                    float ypos = (float) y;
                    g2d.draw(new Line2D.Float(Xpos, ypos, Xpos, ypos));
                    z++;
                }
            }

        }
    }

    void drawPath(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;
        float prvX = 0;
        float prvY = 0;
        g2d.setColor(Color.YELLOW);
        g2d.setColor(new Color(147, 194, 238));

        for (Float[] point : rf.getRoboPath()) {
            if (prvX > 1) {
                g2d.draw(new Line2D.Float(prvX, prvY, point[0], point[1]));
            }
            prvX = point[0];
            prvY = point[1];
        }
    }

    void drawRobo(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;
        int radius = 3;
        Stroke stroke = new BasicStroke(3f);
        g2d.setStroke(stroke);
        g2d.setColor(new Color(75, 235, 149));
        g2d.draw(new Ellipse2D.Double(rf.getRoboX() - radius, rf.getRoboY() - radius, 2.0 * radius, 2.0 * radius));
        radius = 6;
        g2d.setColor(Color.YELLOW);
        g2d.draw(
                new Ellipse2D.Double(rf.getChargerX() - radius, rf.getChargerY() - radius, 2.0 * radius, 2.0 * radius));
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        // g.drawImage(image, 0, 0, this);
        if (rf != null) {
            drawMap(g);
            drawPath(g);
            drawRobo(g);
        }

    }

    @Override
    public Dimension getPreferredSize() {
        return size;
    }

    public void setImage(BufferedImage bi) {
        image = bi;
        setComponentSize();
        repaint();
    }

    private void setComponentSize() {
        if (image != null) {
            size.width = image.getWidth();
            size.height = image.getHeight();
            revalidate(); // signal parent/scrollpane
        }
    }

}

class RRFileParser {
    final static int CHARGER = 1;
    final static int IMAGE = 2;
    final static int PATH = 3;
    final static int GOTO_PATH = 4;
    final static int GOTO_PREDICTED_PATH = 5;
    final static int CURRENTLY_CLEANED_ZONES = 6;
    final static int GOTO_TARGET = 7;
    final static int ROBOT_POSITION = 8;
    final static int NO_GO_AREAS = 9;
    final static int VIRTUAL_WALLS = 10;
    final static int DIGEST = 1024;

    private byte[] image;
    private int majorVersion;
    private int minorVersion;
    private int mapIndex;
    private int mapSequence;

    private int imgHeight;
    private int imgWidth;
    private int imagesize;

    private int chargerX;
    private int chargerY;
    private int roboX;
    private int roboY;
    private int top;
    private int left;
    private int setPointLength;
    private int setPointSize;
    private int setAngle;
    private ArrayList<Float[]> roboPath = new ArrayList<Float[]>();
    final static float MM = 50.0f;
    final static int SIZE = 1024;

    public RRFileParser(byte[] raw) {

        this.majorVersion = getUInt16(raw, 0x08);
        this.minorVersion = getUInt16(raw, 0x0A);
        this.mapIndex = getUInt32LE(raw, 0x0C);
        this.mapSequence = getUInt32LE(raw, 0x10);

        long nextpos = 0x14; // startpos first block after the main header
        while (nextpos < raw.length) {
            byte[] header = getBytes(raw, (int) nextpos, 0x20);
            int blocktype = getUInt16(getBytes(header, 0x00, 2));
            long l = getUInt32LE(header, 0x04);

            switch (blocktype) {
            case CHARGER:
                this.chargerX = getUInt32LE(header, 0x08);
                this.chargerY = getUInt32LE(header, 0x0C);
                break;
            case IMAGE:
                this.setImgHeight((getUInt32LE(header, 0x10)));
                this.top = getUInt32LE(header, 0x08);
                this.left = getUInt32LE(header, 0x0C);
                this.setImgWidth((getUInt32LE(header, 0x14)));
                this.setImagesize(getUInt32LE(header, 0x04));
                this.image = java.util.Arrays.copyOfRange(raw, (int) (nextpos + 0x18), (int) imagesize);
                break;
            case PATH:
                int pairs = getUInt32LE(header, 0x04) / 4;
                this.setPointLength = getUInt32LE(header, 0x08);
                this.setPointSize = getUInt32LE(header, 0x0C);
                this.setAngle = getUInt32LE(header, 0x10);
                long startpos = 0x14 + nextpos;
                for (int pathpair = 0; pathpair < pairs; pathpair++) {
                    Float x = (float) SIZE - (getUInt16(getBytes(raw, (int) (startpos + pathpair * 4), 2))) / MM - left;
                    Float y = getUInt16(getBytes(raw, (int) (startpos + pathpair * 4 + 2), 2)) / MM - top;
                    roboPath.add(new Float[] { x, y });
                }
                break;
            case ROBOT_POSITION:
                this.roboX = getUInt32LE(header, 0x08);
                this.roboY = getUInt32LE(header, 0x0C);
                break;

            case GOTO_PATH:
            case GOTO_PREDICTED_PATH:
            case CURRENTLY_CLEANED_ZONES:
            case GOTO_TARGET:
            case NO_GO_AREAS:
            case VIRTUAL_WALLS:
            case DIGEST:
                System.out.print("Unimplemented blocktype: ");
                System.out.println(blocktype);
                break;

            default: {
                System.out.print("Unknown blocktype: ");
                System.out.println(blocktype);

            }
            }
            nextpos = nextpos + l + (header[2] & 0xFF);
        }
    }

    public byte[] getImage() {
        return image;
    }

    public void setImage(byte[] image) {
        this.image = image;
    }

    public byte[] getBytes(byte[] raw, int pos, int len) {
        return java.util.Arrays.copyOfRange(raw, pos, pos + len);
    }

    public int getUInt32LE(byte[] bytes) {
        return getUInt32LE(bytes, 0);
    }

    public int getUInt32LE(byte[] bytes, int pos) {
        int value = bytes[0 + pos] & 0xFF;
        value |= (bytes[1 + pos] << 8) & 0xFFFF;
        value |= (bytes[2 + pos] << 16) & 0xFFFFFF;
        value |= (bytes[3 + pos] << 24) & 0xFFFFFFFF;
        return value;
    }

    public int getUInt16(byte[] bytes) {
        return getUInt16(bytes, 0);
    }

    public int getUInt16(byte[] bytes, int pos) {
        int value = bytes[0 + pos] & 0xFF;
        value |= (bytes[1 + pos] << 8) & 0xFFFF;
        return value;
    }

    public int getImagesize() {
        return imagesize;
    }

    public void setImagesize(int imagesize) {
        this.imagesize = imagesize;
    }

    public int getImgHeight() {
        return imgHeight;
    }

    public void setImgHeight(int imgHight) {
        this.imgHeight = imgHight;
    }

    public int getImgWidth() {
        return imgWidth;
    }

    public void setImgWidth(int imgWidth) {
        this.imgWidth = imgWidth;
    }

    public int getTop() {
        return top;
    }

    public int getLeft() {
        return left;
    }

    public int getValue() {
        return value;
    }

    public ArrayList<Float[]> getRoboPath() {
        return roboPath;
    }

    public float getRoboX() {
        return (float) SIZE - (roboX / MM) - left;
    }

    public float getRoboY() {
        return (float) roboY / MM - top;
    }

    public float getChargerX() {
        return (float) SIZE - (chargerX / MM) - left;
    }

    public float getChargerY() {
        return (float) chargerY / MM - top;
    }

    public String toSting() {
        String s = "ImageData: Major Version: " + majorVersion + " Minor version: " + minorVersion + " map Index: "
                + mapIndex + " Map Sequence: " + mapSequence + " \r\n" + "Image Size: " + Long.toString(imagesize)
                + " top: " + Long.toString(top) + " left: " + Long.toString(left) + " height: "
                + Long.toString(imgHeight) + " width: " + Long.toString(imgWidth) + "\r\n" + "Charger X:"
                + Long.toString(chargerX) + " Charger Y:" + Long.toString(chargerY) + "\r\n" + "Robo X:"
                + Long.toString(roboX) + " Robo Y:" + Long.toString(roboY) + "\r\n" + "Path: Pairs:"
                + Integer.toString(roboPath.size()) + " PointLenght: " + Integer.toString(setPointLength)
                + " PointSize: " + Integer.toString(setPointSize) + " Angle: " + Integer.toString(setAngle);
        return s;
    }
}
