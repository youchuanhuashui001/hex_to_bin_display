import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QLineEdit, QFrame, QPushButton,
                           QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPalette, QLinearGradient

class BitIndicator(QFrame):
    def __init__(self, bit_number, parent=None):
        super().__init__(parent)
        self.setMinimumSize(40, 30)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.value = False
        self.bit_number = bit_number
        
        # 设置样式
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet("""
            BitIndicator {
                background-color: transparent;
            }
        """)
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setSpacing(1)
        layout.setContentsMargins(1, 1, 1, 1)
        
        # 添加位号标签
        self.bit_label = QLabel(f"Bit {bit_number}")
        self.bit_label.setAlignment(Qt.AlignCenter)
        self.bit_label.setFont(QFont("Segoe UI", 9))
        self.bit_label.setStyleSheet("color: #9e9e9e;")
        layout.addWidget(self.bit_label)
        
        # 创建状态指示器
        self.indicator = QFrame()
        self.indicator.setFixedSize(40, 3)
        self.indicator.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-radius: 1px;
            }
        """)
        layout.addWidget(self.indicator, 0, Qt.AlignCenter)
        
    def setValue(self, value):
        self.value = value
        if value:
            self.indicator.setStyleSheet("""
                QFrame {
                    background-color: #4CAF50;
                    border-radius: 3px;
                }
            """)
        else:
            self.indicator.setStyleSheet("""
                QFrame {
                    background-color: #f44336;
                    border-radius: 3px;
                }
            """)

class ByteGroup(QFrame):
    def __init__(self, byte_number, parent=None):
        super().__init__(parent)
        self.byte_number = byte_number
        self.bits = []
        
        # 设置大小策略
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # 设置样式
        self.setStyleSheet("""
            ByteGroup {
                background-color: #1a1a1a;
                border-radius: 8px;
                border: 1px solid #2d2d2d;
            }
            ByteGroup:hover {
                background-color: #202020;
                border: 1px solid #3d3d3d;
            }
        """)
        
        # 创建布局
        layout = QHBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(10, 6, 10, 6)
        
        # 添加字节标签和值
        byte_frame = QFrame()
        byte_frame.setFixedWidth(80)
        byte_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-radius: 4px;
            }
        """)
        byte_layout = QVBoxLayout(byte_frame)
        byte_layout.setContentsMargins(4, 4, 4, 4)
        byte_layout.setSpacing(1)
        
        # 添加字节标签
        byte_label = QLabel(f"Byte {byte_number}")
        byte_label.setFont(QFont("Segoe UI", 9))
        byte_label.setStyleSheet("color: #9e9e9e;")
        byte_label.setAlignment(Qt.AlignCenter)
        byte_layout.addWidget(byte_label)
        
        # 添加16进制值显示
        self.hex_value = QLabel("0x00")
        self.hex_value.setFont(QFont("Segoe UI", 8))
        self.hex_value.setStyleSheet("color: #757575;")
        self.hex_value.setAlignment(Qt.AlignCenter)
        byte_layout.addWidget(self.hex_value)
        
        layout.addWidget(byte_frame)
        
        # 添加位指示器
        bits_frame = QFrame()
        bits_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        bits_frame.setStyleSheet("background: transparent;")
        bits_layout = QHBoxLayout(bits_frame)
        bits_layout.setSpacing(4)
        bits_layout.setContentsMargins(0, 0, 0, 0)
        
        for i in range(8):
            bit = BitIndicator(7 - i)
            self.bits.append(bit)
            bits_layout.addWidget(bit)
            
        layout.addWidget(bits_frame, 1)
            
    def setByteValue(self, value):
        # 更新16进制值显示
        self.hex_value.setText(f"0x{value:02X}")
        # 更新每个位的显示
        bin_str = format(value, '08b')
        for i, bit in enumerate(self.bits):
            bit.setValue(bin_str[i] == '1')

class ModernLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                color: #e0e0e0;
                font-size: 14px;
                selection-background-color: #0288d1;
            }
            QLineEdit:focus {
                border: 2px solid #0288d1;
                background-color: #333333;
            }
            QLineEdit:hover {
                background-color: #333333;
            }
        """)

class BinaryDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('16进制数据显示器')
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QLabel {
                color: #e0e0e0;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建输入区域（居中对齐）
        input_frame = QFrame()
        input_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-radius: 8px;
                border: 1px solid #2d2d2d;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建水平布局用于居中对齐
        input_container = QHBoxLayout()
        
        # 创建一个包含标签和输入框的垂直布局
        input_content = QVBoxLayout()
        input_content.setSpacing(6)
        
        input_label = QLabel('输入16进制数据 (最大64位/8字节)：')
        input_label.setFont(QFont("Segoe UI", 10))
        input_label.setStyleSheet("color: #e0e0e0;")
        input_label.setAlignment(Qt.AlignCenter)
        input_content.addWidget(input_label)
        
        self.input_field = ModernLineEdit()
        self.input_field.setFixedWidth(300)
        self.input_field.setFont(QFont("Segoe UI", 10))
        self.input_field.textChanged.connect(self.updateDisplay)
        input_content.addWidget(self.input_field, 0, Qt.AlignCenter)
        
        input_container.addStretch()
        input_container.addLayout(input_content)
        input_container.addStretch()
        
        input_layout.addLayout(input_container)
        main_layout.addWidget(input_frame)
        
        # 创建字节组显示区域
        display_widget = QWidget()
        display_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        display_widget.setStyleSheet("background: transparent;")
        display_layout = QVBoxLayout(display_widget)
        display_layout.setContentsMargins(0, 0, 0, 0)
        display_layout.setSpacing(4)
        
        self.byte_groups = []
        # 从7到0创建字节组，保持显示顺序
        for i in range(8):
            byte_group = ByteGroup(7 - i)  # 从Byte7开始
            self.byte_groups.append(byte_group)  # 添加到列表末尾
            display_layout.addWidget(byte_group)
        
        main_layout.addWidget(display_widget)
        
        # 设置窗口尺寸
        self.setMinimumSize(600, 600)
        self.resize(600, 600)

    def updateDisplay(self):
        try:
            # 获取输入的16进制字符串并移除0x前缀
            hex_str = self.input_field.text().strip().lower().replace('0x', '')
            if not hex_str:
                # 如果输入为空，重置所有显示
                for byte_group in self.byte_groups:
                    byte_group.setByteValue(0)
                self.input_field.setStyleSheet(ModernLineEdit().styleSheet())
                return
                
            # 转换为整数
            value = int(hex_str, 16)
            
            # 检查是否超过64位
            if value.bit_length() > 64:
                self.input_field.setStyleSheet("""
                    QLineEdit {
                        padding: 12px;
                        background-color: #2d2d2d;
                        border: 2px solid #c62828;
                        border-radius: 8px;
                        color: #e0e0e0;
                        font-size: 14px;
                    }
                """)
                return
                
            # 重置输入框样式
            self.input_field.setStyleSheet(ModernLineEdit().styleSheet())
            
            # 更新显示 - 修改字节顺序
            # 创建一个8字节的列表，初始化为0
            bytes_list = [0] * 8
            
            # 从低位到高位提取每个字节
            for i in range(8):
                bytes_list[i] = (value >> (i * 8)) & 0xFF
            
            # 更新每个字节组的显示
            for i in range(8):
                self.byte_groups[7-i].setByteValue(bytes_list[i])
                
        except ValueError:
            # 输入无效时显示错误样式
            self.input_field.setStyleSheet("""
                QLineEdit {
                    padding: 12px;
                    background-color: #2d2d2d;
                    border: 2px solid #c62828;
                    border-radius: 8px;
                    color: #e0e0e0;
                    font-size: 14px;
                }
            """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion风格
    window = BinaryDisplay()
    window.show()
    sys.exit(app.exec_()) 