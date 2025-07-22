<!-- README Template for MiniPilot Project -->
<h1 align="center">MiniPilot 🚗🤖</h1>
<p align="center">
  <em>Autonomous robot powered by Raspberry Pi 4 and YOLOv5n</em>
</p>
<hr/>

<h2>📚 Documentation</h2>
<ul>
  <li><a href="#project-overview">Project Overview</a></li>
  <li><a href="#hardware-requirements">Hardware Requirements</a></li>
  <li><a href="#software-stack">Software Stack</a></li>
  <li><a href="#getting-started">Getting Started</a></li>
  <li><a href="#usage-examples">Usage Examples</a></li>
  <li><a href="#contributing">Contributing</a></li>
</ul>

<h2>🌟 Project Overview</h2>
<p>
  <strong>MiniPilot</strong> is a DIY robot platform leveraging a custom-trained <a href="https://github.com/ultralytics/yolov5">YOLOv5n</a> neural network for object detection and navigation. Built on a Raspberry Pi 4, MiniPilot aims to provide a simple yet powerful starting point for robotics and AI enthusiasts.
</p>

<h2>🛠️ Features</h2>
<ul>
  <li>Real-time object detection with YOLOv5n</li>
  <li>Custom-trained model for specific environments</li>
  <li>Raspberry Pi 4 hardware integration</li>
  <li>Modular Python codebase</li>
  <li>Easy to extend for your own robot builds</li>
</ul>

<h2>📦 Hardware Stack</h2>
<ul>
  <li>Raspberry Pi </li>
  <li>USB Camera (compatible with Pi)</li>
  <li>Motors and motor driver (e.g., L298N)</li>
  <li>Chassis & wheels</li>
  <li>Power supply (8x AA)</li>
  <li>Ultrasonic sensors, IR sensors</li>
</ul>

<h2>💻 Software Stack</h2>
<ul>
  <li>Python 3.10</li>
  <li>PyTorch</li>
  <li>YOLOv5n (custom-trained weights)</li>
  <li>OpenCV for image processing</li>
  <li>GPIO libraries for hardware control</li>
</ul>

<h2>🚀 Getting Started</h2>
<ol>
  <li>Clone this repository:
    <pre><code>git clone https://github.com/Cwalt2/yolov5-x-MiniPilot.git</code></pre>
  </li>
  <li>Install dependencies:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>Download your custom YOLOv5n weights and place them in the <code>weights/</code> directory or use the custom trained model <code>traffic.pt</code>.</li>
  <li>Connect your Pi4 to the robot hardware as per <a href="#hardware-requirements">Hardware Requirements</a>.</li>
  <li>Run the hardware movement script:
    <pre><code>python ir_move.py</code></pre>
  </li>
    <li>Run the AI detect script:
    <div>
    On Windows:
    <pre><code>python .\detect.py --weights best.pt --source 0 --img 640 --conf 0.4 --device cpu --save-txt --project runs/detect --name exp --exist-ok</code></pre>
    </div>
        <div>
    On Linux:
    <pre><code>python detect-linux.py --weights best.pt --source 0 --img 640 --conf 0.4 --device cpu --save-txt --project runs/detect --name exp --exist-ok</code></pre>
    </div>
  </li>
</ol>

<h2>🖼️ Usage Examples</h2>
<p>
  <img src="docs/images/demo.jpg" alt="MiniPilot in action" width="600"/>
</p>
<pre><code>
# Run detection
python minipilot.py --source 0 --weights weights/custom_yolov5n.pt
</code></pre>

<h2 class="#contributing">🤝 Contributing</h2>
<p>
  Pull requests are welcome! For major changes, open an issue first to discuss what you would like to change.
</p>
