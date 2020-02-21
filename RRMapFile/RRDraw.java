package RRMap;

import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Transparency;
import java.awt.color.ColorSpace;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
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
        super("File View Test Frame");
        setSize(350, 400);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        parent = this;
        rrDrawPanel = new RRDrawPanel();
        Container c = getContentPane();
        // The default BorderLayout will work better.
        // c.setLayout(new FlowLayout());

        JButton openButton = new JButton("Open");
        final JLabel statusbar = new JLabel("Output of your selection will go here");

        openButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent ae) {
                JFileChooser chooser = new JFileChooser("images");

                int option = chooser.showOpenDialog(parent);
                if (option == JFileChooser.APPROVE_OPTION) {
                    File file = chooser.getSelectedFile();
                    // File file = "c:\\temp\\map01.gz";
                    BufferedImage loadImage = loadImage(file);
                    statusbar.setText(file.getName() + " size " + loadImage.getWidth() + "x" + loadImage.getHeight());
                    // setSize(loadImage.getWidth(), loadImage.getHeight());
                    rrDrawPanel.setSize(loadImage.getHeight(), loadImage.getWidth());
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
    private BufferedImage loadImage(File file) {
        BufferedImage image = null;
        try {

            byte[] inputdata = readGZFile(file);
            RRFileDecoder rf = new RRFileDecoder(inputdata);
            System.out.println(rf.toSting());
            int l = (int) rf.getImgHeight();
            int w = (int) rf.getImgWidth();
            byte[] buffer = rf.getImage();
            setSize(w, l);
            // BufferedImage bufferedImage = new BufferedImage(l, w, BufferedImage.TYPE_BYTE_GRAY);
            image = flipHoriz(getGrayscale(l, buffer));

            // image = ImageIO.read(file);
        } catch (IOException e) {
            System.out.println("read error: " + e.getMessage());
        }
        if (image != null) {
            rrDrawPanel.setImage(image);
        }
        return image;
    }

    public static void main(String args[]) {
        System.setProperty("swing.defaultlaf", "javax.swing.plaf.metal.MetalLookAndFeel");
        RRDraw vc = new RRDraw();
        vc.setVisible(true);
    }

    public static BufferedImage flipHoriz(BufferedImage image) {
        BufferedImage newImage = new BufferedImage(image.getWidth(), image.getHeight(), BufferedImage.TYPE_INT_ARGB);
        Graphics2D gg = newImage.createGraphics();
        gg.drawImage(image, image.getHeight(), 0, -image.getWidth(), image.getHeight(), null);
        gg.dispose();
        return newImage;
    }

    /**
     *
     * @param width The image width (height derived from buffer length)
     * @param buffer The buffer containing raw grayscale pixel data
     *
     * @return THe grayscale image
     */
    public static BufferedImage getGrayscale(int width, byte[] buffer) {
        int height = buffer.length / width;
        ColorSpace cs = ColorSpace.getInstance(ColorSpace.CS_GRAY);
        int[] nBits = { 8 };
        ColorModel cm = new ComponentColorModel(cs, nBits, false, true, Transparency.OPAQUE, DataBuffer.TYPE_BYTE);
        SampleModel sm = cm.createCompatibleSampleModel(width, height);
        DataBufferByte db = new DataBufferByte(buffer, width * height);
        WritableRaster raster = Raster.createWritableRaster(sm, db, null);
        BufferedImage result = new BufferedImage(cm, raster, false, null);
        return result;
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

    public RRDrawPanel() {
    }

    public RRDrawPanel(BufferedImage image) {
        this.image = image;
        setComponentSize();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.drawImage(image, 0, 0, this);
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

class RRFileDecoder {
    private byte[] image;
    private long imgHeight;
    private long imgWidth;
    private long imagesize;

    public RRFileDecoder(byte[] raw) {
        nextBlock(raw);
        // this.setImgHeight((getUInt32(getBytes(raw, 0x38, 4))));
        // this.setImgWidth((getUInt32(getBytes(raw, 0x34, 4))));
        // this.setImagesize(getUInt32(getBytes(raw, 0x28, 4)));
        // this.image = java.util.Arrays.copyOfRange(raw, 0x3A, (int) imagesize);
    }

    private void nextBlock(byte[] raw) {
        long nextpos = 0x14;
        while (nextpos < raw.length) {
            byte[] header = getBytes(raw, (int) nextpos, 0x20);
            int blocktype = header[0] & 0xFF + 256 * (header[1] & 0xFF);
            System.out.print("Block: ");
            System.out.print(blocktype);
            System.out.print(" loc ");
            System.out.print(nextpos);
            System.out.print(" len: ");
            long l = getUInt32(getBytes(header, 0x04, 4));
            System.out.println(l);

            if (blocktype == 2) { // block 2 = image
                this.setImgHeight((getUInt32(getBytes(header, 0x14, 4))));
                this.setImgWidth((getUInt32(getBytes(header, 0x10, 4))));
                this.setImagesize(getUInt32(getBytes(header, 0x04, 4)));
                this.image = java.util.Arrays.copyOfRange(raw, (int) (nextpos + 0x18), (int) imagesize);
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

    public long getUInt32(byte[] bytes) {
        long value = bytes[0] & 0xFF;
        value |= (bytes[1] << 8) & 0xFFFF;
        value |= (bytes[2] << 16) & 0xFFFFFF;
        value |= (bytes[3] << 24) & 0xFFFFFFFF;
        return value;
    }

    public long getImagesize() {
        return imagesize;
    }

    public void setImagesize(long imagesize) {
        this.imagesize = imagesize;
    }

    public long getImgHeight() {
        return imgHeight;
    }

    public void setImgHeight(long imgHight) {
        this.imgHeight = imgHight;
    }

    public long getImgWidth() {
        return imgWidth;
    }

    public void setImgWidth(long imgWidth) {
        this.imgWidth = imgWidth;
    }

    public String toSting() {
        String s = "Image Size: " + Long.toString(imagesize) + " height: " + Long.toString(imgHeight) + " width: "
                + Long.toString(imgWidth);
        return s;
    }
}
