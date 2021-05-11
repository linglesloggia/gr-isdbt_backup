#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Full Transceiver Isdbt
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio import digital
from gnuradio import dtv
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import isdbt
import numpy as np
from gnuradio import qtgui

class full_transceiver_isdbt(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Full Transceiver Isdbt")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Full Transceiver Isdbt")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "full_transceiver_isdbt")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 8e6*64/63
        self.mode = mode = 3
        self.total_carriers = total_carriers = 2**(10+mode)
        self.throttle_rate = throttle_rate = samp_rate/1.0
        self.segments_c = segments_c = 0
        self.segments_b = segments_b = 0
        self.segments_a = segments_a = 13
        self.phase_noise = phase_noise = 0
        self.noise = noise = 1e-9
        self.max_doppler = max_doppler = 0
        self.length_c = length_c = 0
        self.length_b = length_b = 2
        self.length_a = length_a = 4
        self.iip3 = iip3 = 50
        self.guard = guard = 1.0/16
        self.freq_error = freq_error = 0
        self.epsilon = epsilon = 1
        self.data_carriers = data_carriers = 13*96*2**(mode-1)
        self.bb_gain = bb_gain = 0.0022097087*2
        self.active_carriers = active_carriers = 13*108*2**(mode-1)+1

        ##################################################
        # Blocks
        ##################################################
        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, 'Diagrama IQ')
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, 'Espectro en recepcion')
        self.tab_widget_2 = Qt.QWidget()
        self.tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_2)
        self.tab_grid_layout_2 = Qt.QGridLayout()
        self.tab_layout_2.addLayout(self.tab_grid_layout_2)
        self.tab.addTab(self.tab_widget_2, 'Constelacion en recepcion')
        self.tab_widget_3 = Qt.QWidget()
        self.tab_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_3)
        self.tab_grid_layout_3 = Qt.QGridLayout()
        self.tab_layout_3.addLayout(self.tab_grid_layout_3)
        self.tab.addTab(self.tab_widget_3, 'Transferencia Canal (magnitud)')
        self.tab_widget_4 = Qt.QWidget()
        self.tab_layout_4 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_4)
        self.tab_grid_layout_4 = Qt.QGridLayout()
        self.tab_layout_4.addLayout(self.tab_grid_layout_4)
        self.tab.addTab(self.tab_widget_4, 'Respuesta impulso Canal')
        self.top_grid_layout.addWidget(self.tab, 0, 1, 8, 4)
        for r in range(0, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._phase_noise_range = Range(0, 5, 1e-6, 0, 200)
        self._phase_noise_win = RangeWidget(self._phase_noise_range, self.set_phase_noise, 'Ruido de fase', "counter_slider", float)
        self.top_grid_layout.addWidget(self._phase_noise_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_range = Range(1e-9, 0.5, 1e-6, 1e-9, 200)
        self._noise_win = RangeWidget(self._noise_range, self.set_noise, 'Ruido en el canal', "counter_slider", float)
        self.top_grid_layout.addWidget(self._noise_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._iip3_range = Range(-20, 50, 1, 50, 200)
        self._iip3_win = RangeWidget(self._iip3_range, self.set_iip3, 'Distorsion de orden tres (IIP3, dB)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._iip3_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_error_range = Range(-1, 1, 1e-5, 0, 200)
        self._freq_error_win = RangeWidget(self._freq_error_range, self.set_freq_error, 'Error en frecuencia (% samp_rate)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_error_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._epsilon_range = Range(1-1e-4, 1+1e-4, 1e-6, 1, 200)
        self._epsilon_win = RangeWidget(self._epsilon_range, self.set_epsilon, 'Error de muestreo (% samp_rate)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._epsilon_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            101, #size
            samp_rate, #samp_rate
            "Respuesta al impulso estimada (primeros 101 taps)", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(True)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.tab_layout_4.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_1.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_const_sink_x_1 = qtgui.const_sink_c(
            200, #size
            "", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_1.set_update_time(0.10)
        self.qtgui_const_sink_x_1.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_1.enable_autoscale(False)
        self.qtgui_const_sink_x_1.enable_grid(False)
        self.qtgui_const_sink_x_1.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [1, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [-1, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_1_win = sip.wrapinstance(self.qtgui_const_sink_x_1.pyqwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._qtgui_const_sink_x_1_win)
        self._max_doppler_range = Range(0, 50, 0.2, 0, 200)
        self._max_doppler_win = RangeWidget(self._max_doppler_range, self.set_max_doppler, 'Doppler Spread (Hz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._max_doppler_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                5.8e6/2.0,
                0.5e6,
                firdes.WIN_HAMMING,
                6.76))
        self.isdbt_tmcc_encoder_0 = isdbt.tmcc_encoder(3, True, 4, 4, 4, 0, 0, 0, 2, 0, 0, 13, 0, 0)
        self.isdbt_tmcc_decoder_0 = isdbt.tmcc_decoder(3, True)
        self.isdbt_time_interleaver_0 = isdbt.time_interleaver(3, 13, 2, 0, 0, 0, 0)
        self.isdbt_time_deinterleaver_0 = isdbt.time_deinterleaver(3, 13, 2, 0, 0, 0, 0)
        self.isdbt_symbol_demapper_0 = isdbt.symbol_demapper(3, 13, 4, 0, 4, 0, 4)
        self.isdbt_subset_of_carriers_0 = isdbt.subset_of_carriers(5617, 0, 100)
        self.isdbt_pilot_signals_0 = isdbt.pilot_signals(3)
        self.isdbt_ofdm_synchronization_0 = isdbt.ofdm_synchronization(3, 0.250, True)
        self.isdbt_hierarchical_combinator_0 = isdbt.hierarchical_combinator(3, 13, 0, 0)
        self.isdbt_frequency_interleaver_0 = isdbt.frequency_interleaver(False, 3)
        self.isdbt_frequency_deinterleaver_0 = isdbt.frequency_deinterleaver(False, 3)
        self.isdbt_energy_dispersal_0 = isdbt.energy_dispersal(3, 4, 0, 13)
        self.isdbt_energy_descrambler_0 = isdbt.energy_descrambler()
        self.isdbt_carrier_modulation_0 = isdbt.carrier_modulation(3, 13, 4)
        self.isdbt_byte_interleaver_0 = isdbt.byte_interleaver(3, 4, 0, 13)
        self.isdbt_byte_deinterleaver_0 = isdbt.byte_deinterleaver()
        self.isdbt_bit_deinterleaver_0 = isdbt.bit_deinterleaver(3, 13, 4)
        self.fft_vxx_1 = fft.fft_vcc(total_carriers, False, window.rectangular(total_carriers), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(active_carriers, False, window.rectangular(active_carriers), True, 1)
        self.dtv_dvbt_viterbi_decoder_0_0 = dtv.dvbt_viterbi_decoder(dtv.MOD_QPSK, dtv.ALPHA4, dtv.C1_2, 204)
        self.dtv_dvbt_reed_solomon_enc_0 = dtv.dvbt_reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, 1)
        self.dtv_dvbt_reed_solomon_dec_0_0 = dtv.dvbt_reed_solomon_dec(2, 8, 0x11d, 255, 239, 8, 51, 1)
        self.dtv_dvbt_inner_coder_0_0 = dtv.dvbt_inner_coder(1, 1512*4, dtv.MOD_QPSK, dtv.ALPHA4, dtv.C1_2)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(total_carriers, total_carriers + int(total_carriers*guard), 0, '')
        self.channels_phase_noise_gen_0 = channels.phase_noise_gen(phase_noise, 0.01)
        self.channels_distortion_3_gen_0 = channels.distortion_3_gen(-0.11/10**(iip3/10.0))
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise,
            frequency_offset=freq_error,
            epsilon=epsilon,
            taps=[1],
            noise_seed=0,
            block_tags=False)
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 101)
        self.blocks_vector_to_stream_0_1 = blocks.vector_to_stream(gr.sizeof_char*1, 1512*4)
        self.blocks_vector_to_stream_0_0_0 = blocks.vector_to_stream(gr.sizeof_char*1, 188)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, throttle_rate,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, 188)
        self.blocks_skiphead_0_0 = blocks.skiphead(gr.sizeof_gr_complex*data_carriers, 2)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(bb_gain, 1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/lingles/fing/gr-isdbt/layer_a.ts', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, '/home/lingles/fing/gr-isdbt/layer_a_out.ts', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_skiphead_0_0, 0), (self.isdbt_pilot_signals_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.dtv_dvbt_reed_solomon_enc_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.channels_phase_noise_gen_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.qtgui_const_sink_x_1, 0))
        self.connect((self.blocks_vector_to_stream_0_0_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1, 0), (self.isdbt_carrier_modulation_0, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.channels_channel_model_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.channels_distortion_3_gen_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.channels_phase_noise_gen_0, 0), (self.channels_distortion_3_gen_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.dtv_dvbt_inner_coder_0_0, 0), (self.blocks_vector_to_stream_0_1, 0))
        self.connect((self.dtv_dvbt_reed_solomon_dec_0_0, 0), (self.blocks_vector_to_stream_0_0_0, 0))
        self.connect((self.dtv_dvbt_reed_solomon_enc_0, 0), (self.isdbt_energy_dispersal_0, 0))
        self.connect((self.dtv_dvbt_viterbi_decoder_0_0, 0), (self.isdbt_byte_deinterleaver_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.isdbt_subset_of_carriers_0, 0))
        self.connect((self.fft_vxx_1, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))
        self.connect((self.isdbt_bit_deinterleaver_0, 0), (self.dtv_dvbt_viterbi_decoder_0_0, 0))
        self.connect((self.isdbt_byte_deinterleaver_0, 0), (self.isdbt_energy_descrambler_0, 0))
        self.connect((self.isdbt_byte_interleaver_0, 0), (self.dtv_dvbt_inner_coder_0_0, 0))
        self.connect((self.isdbt_carrier_modulation_0, 0), (self.isdbt_hierarchical_combinator_0, 0))
        self.connect((self.isdbt_energy_descrambler_0, 0), (self.dtv_dvbt_reed_solomon_dec_0_0, 0))
        self.connect((self.isdbt_energy_dispersal_0, 0), (self.isdbt_byte_interleaver_0, 0))
        self.connect((self.isdbt_frequency_deinterleaver_0, 0), (self.isdbt_time_deinterleaver_0, 0))
        self.connect((self.isdbt_frequency_interleaver_0, 0), (self.blocks_skiphead_0_0, 0))
        self.connect((self.isdbt_hierarchical_combinator_0, 0), (self.isdbt_time_interleaver_0, 0))
        self.connect((self.isdbt_ofdm_synchronization_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.isdbt_ofdm_synchronization_0, 0), (self.isdbt_tmcc_decoder_0, 0))
        self.connect((self.isdbt_pilot_signals_0, 0), (self.isdbt_tmcc_encoder_0, 0))
        self.connect((self.isdbt_subset_of_carriers_0, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.isdbt_symbol_demapper_0, 0), (self.isdbt_bit_deinterleaver_0, 0))
        self.connect((self.isdbt_time_deinterleaver_0, 0), (self.isdbt_symbol_demapper_0, 0))
        self.connect((self.isdbt_time_interleaver_0, 0), (self.isdbt_frequency_interleaver_0, 0))
        self.connect((self.isdbt_tmcc_decoder_0, 0), (self.isdbt_frequency_deinterleaver_0, 0))
        self.connect((self.isdbt_tmcc_encoder_0, 0), (self.fft_vxx_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.isdbt_ofdm_synchronization_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "full_transceiver_isdbt")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_throttle_rate(self.samp_rate/1.0)
        self.channels_selective_fading_model_0.set_fDTs(self.max_doppler/self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 5.8e6/2.0, 0.5e6, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode
        self.set_active_carriers(13*108*2**(self.mode-1)+1)
        self.set_data_carriers(13*96*2**(self.mode-1))
        self.set_total_carriers(2**(10+self.mode))

    def get_total_carriers(self):
        return self.total_carriers

    def set_total_carriers(self, total_carriers):
        self.total_carriers = total_carriers

    def get_throttle_rate(self):
        return self.throttle_rate

    def set_throttle_rate(self, throttle_rate):
        self.throttle_rate = throttle_rate
        self.blocks_throttle_0_0.set_sample_rate(self.throttle_rate)

    def get_segments_c(self):
        return self.segments_c

    def set_segments_c(self, segments_c):
        self.segments_c = segments_c

    def get_segments_b(self):
        return self.segments_b

    def set_segments_b(self, segments_b):
        self.segments_b = segments_b

    def get_segments_a(self):
        return self.segments_a

    def set_segments_a(self, segments_a):
        self.segments_a = segments_a

    def get_phase_noise(self):
        return self.phase_noise

    def set_phase_noise(self, phase_noise):
        self.phase_noise = phase_noise
        self.channels_phase_noise_gen_0.set_noise_mag(self.phase_noise)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.channels_channel_model_0.set_noise_voltage(self.noise)

    def get_max_doppler(self):
        return self.max_doppler

    def set_max_doppler(self, max_doppler):
        self.max_doppler = max_doppler
        self.channels_selective_fading_model_0.set_fDTs(self.max_doppler/self.samp_rate)

    def get_length_c(self):
        return self.length_c

    def set_length_c(self, length_c):
        self.length_c = length_c

    def get_length_b(self):
        return self.length_b

    def set_length_b(self, length_b):
        self.length_b = length_b

    def get_length_a(self):
        return self.length_a

    def set_length_a(self, length_a):
        self.length_a = length_a

    def get_iip3(self):
        return self.iip3

    def set_iip3(self, iip3):
        self.iip3 = iip3
        self.channels_distortion_3_gen_0.set_beta(-0.11/10**(self.iip3/10.0))

    def get_guard(self):
        return self.guard

    def set_guard(self, guard):
        self.guard = guard

    def get_freq_error(self):
        return self.freq_error

    def set_freq_error(self, freq_error):
        self.freq_error = freq_error
        self.channels_channel_model_0.set_frequency_offset(self.freq_error)

    def get_epsilon(self):
        return self.epsilon

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon
        self.channels_channel_model_0.set_timing_offset(self.epsilon)

    def get_data_carriers(self):
        return self.data_carriers

    def set_data_carriers(self, data_carriers):
        self.data_carriers = data_carriers

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.blocks_multiply_const_xx_0.set_k(self.bb_gain)

    def get_active_carriers(self):
        return self.active_carriers

    def set_active_carriers(self, active_carriers):
        self.active_carriers = active_carriers



def main(top_block_cls=full_transceiver_isdbt, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
