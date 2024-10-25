# -*- coding: utf-8 -*-
from burp import IBurpExtender
from burp import ITab
from javax.swing import JPanel, JButton, JTextField, JLabel, JFileChooser, JOptionPane
import subprocess
import os

SETTINGS_FILE = "burp_settings.txt"

class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Passive Scanner")
        self.initUI()
        self.loadSettings()
        callbacks.addSuiteTab(self)

    def initUI(self):
        self.panel = JPanel()
        self.panel.setLayout(None)
        self.label_path = JLabel("Path to xray.exe:")
        self.label_path.setBounds(10, 10, 150, 25)
        self.panel.add(self.label_path)

        self.path_field = JTextField(30)
        self.path_field.setBounds(150, 10, 290, 25)
        self.panel.add(self.path_field)

        self.browse_button = JButton("Browse", actionPerformed=self.browseFile)
        self.browse_button.setBounds(450, 10, 80, 25)
        self.panel.add(self.browse_button)
        self.label_command = JLabel("Command:")
        self.label_command.setBounds(10, 50, 150, 25)
        self.panel.add(self.label_command)

        self.command_field = JTextField(30)
        self.command_field.setBounds(150, 50, 290, 25)
        self.panel.add(self.command_field)
        self.run_button = JButton("Run", actionPerformed=self.runTool)
        self.run_button.setBounds(150, 90, 80, 25)
        self.panel.add(self.run_button)

    def getTabCaption(self):
        return "Passive Scanner"

    def getUiComponent(self):
        return self.panel

    def browseFile(self, event):
        chooser = JFileChooser()
        chooser.setFileSelectionMode(JFileChooser.FILES_ONLY)
        result = chooser.showOpenDialog(None)
        if result == JFileChooser.APPROVE_OPTION:
            selected_file = chooser.getSelectedFile()
            self.path_field.setText(selected_file.getAbsolutePath())

    def runTool(self, event):
        path = self.path_field.getText()
        command = self.command_field.getText()

        if not path or not command:
            JOptionPane.showMessageDialog(None, "Please set both the path and command.", "Error", JOptionPane.ERROR_MESSAGE)
            return

        try:
            xray_dir = os.path.dirname(path)
            xray_exe = os.path.basename(path)
            full_command = 'cd /d {} && {} {}'.format(xray_dir, xray_exe, command)
            print(full_command)
            subprocess.Popen(['cmd.exe', '/c', 'start', 'cmd.exe', '/k', full_command])            
            self.saveSettings(path, command)
        except Exception as e:
            error_message = "Error executing command: {}".format(str(e))
            JOptionPane.showMessageDialog(None, error_message, "Error", JOptionPane.ERROR_MESSAGE)

    def saveSettings(self, path, command):
        with open(SETTINGS_FILE, 'w') as settings_file:
            settings_file.write("{}\n{}\n".format(path, command))

    def loadSettings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as settings_file:
                lines = settings_file.readlines()
                if len(lines) >= 2:
                    self.path_field.setText(lines[0].strip())
                    self.command_field.setText(lines[1].strip())
