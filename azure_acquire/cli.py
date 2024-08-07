"""
CLI for acquiring data using Kinect Azure
"""

import os
import click
from azure_acquire.util import start_recording_RT

orig_init = click.core.Option.__init__

def new_init(self, *args, **kwargs):
    orig_init(self, *args, **kwargs)
    self.show_default = True

click.core.Option.__init__ = new_init

@click.version_option()
@click.command(help='start recording depth and IR video')
@click.argument('base-dir', type=click.Path(), default=os.getcwd())
@click.option('--subject-name', help='subject name of the recording')
@click.option('--session-name', help='session name of the recording')
@click.option('--recording-length', '-t', type=float, default = 30, help="recording time (minutes)")
@click.option('--serial-number', '-sn', type=str, help='device serial number')
@click.option('--save-ir', default=True, type=bool, help='save IR video')
@click.option('--preview', default=True, type=bool, help='show frame preview during recording')
@click.option('--display-time', default=True, type=bool, help='show time during the recording')
def record(base_dir, subject_name, session_name, save_ir, recording_length, serial_number, preview, display_time):
    # make base_dir if it doesn't exist
    os.makedirs(base_dir, exist_ok=True)
    #change recording time from minutes to seconds
    recording_length = recording_length * 60

    # prompt user to input session metadata
    if subject_name is None:
        subject_name=input('Input subject name of the recording: ')
    if session_name is None:
        session_name=input('Input session name of the recording: ')

    # prompt users to input serial number when there are multiple devices
    from pyk4a import connected_device_count
    if serial_number is None:
        if connected_device_count() > 1:
            serial_number=input('Input the serial number of the recording device: ')

    start_recording_RT(base_dir=base_dir, subject_name = subject_name, session_name = session_name, 
                       recording_length = recording_length, serial_number=serial_number, save_ir = save_ir,
                       display_frames = preview, display_time = display_time)