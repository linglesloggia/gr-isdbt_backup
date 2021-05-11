#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Qpsk Transceiver Isdbt
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
from gnuradio import dtv
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
import isdbt
import numpy as np
from gnuradio import qtgui

class qpsk_transceiver_isdbt(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Qpsk Transceiver Isdbt")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Qpsk Transceiver Isdbt")
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

        self.settings = Qt.QSettings("GNU Radio", "qpsk_transceiver_isdbt")

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
        self.mode = mode = 3
        self.total_carriers = total_carriers = 2**(10+mode)
        self.samp_rate_estandar = samp_rate_estandar = 8e6*64/63
        self.guard = guard = 1.0/16
        self.data_carriers = data_carriers = 13*96*2**(mode-1)
        self.sym_rate = sym_rate = samp_rate_estandar*data_carriers/((1+guard)*total_carriers)
        self.samp_per_sym = samp_per_sym = 5
        self.samp_rate = samp_rate = sym_rate*samp_per_sym
        self.len_sym_srrc = len_sym_srrc = 15
        self.alfa = alfa = 0.25
        self.throttle_rate = throttle_rate = samp_rate/1.0
        self.segments_c = segments_c = 0
        self.segments_b = segments_b = 0
        self.segments_a = segments_a = 13
        self.pulso_srrc = pulso_srrc = firdes.root_raised_cosine(np.sqrt(samp_per_sym),samp_rate,samp_rate/samp_per_sym,alfa,len_sym_srrc*samp_per_sym)
        self.phase_noise = phase_noise = 0
        self.noise = noise = 1e-9
        self.length_c = length_c = 0
        self.length_b = length_b = 2
        self.length_a = length_a = 4
        self.iip3 = iip3 = 50
        self.freq_error = freq_error = 0
        self.epsilon = epsilon = 1
        self.d = d = 0
        self.const_size = const_size = 64
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
        self.top_grid_layout.addWidget(self.tab, 0, 1, 8, 4)
        for r in range(0, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._phase_noise_range = Range(0, 5, 1e-6, 0, 200)
        self._phase_noise_win = RangeWidget(self._phase_noise_range, self.set_phase_noise, 'Ruido de fase', "counter_slider", float)
        self.top_grid_layout.addWidget(self._phase_noise_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_range = Range(1e-9, 0.5, 1e-6, 1e-9, 200)
        self._noise_win = RangeWidget(self._noise_range, self.set_noise, 'Ruido en el canal', "counter_slider", float)
        self.top_grid_layout.addWidget(self._noise_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._iip3_range = Range(-20, 50, 1, 50, 200)
        self._iip3_win = RangeWidget(self._iip3_range, self.set_iip3, 'Distorsion de orden tres (IIP3, dB)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._iip3_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_error_range = Range(-1, 1, 1e-5, 0, 200)
        self._freq_error_win = RangeWidget(self._freq_error_range, self.set_freq_error, 'Error en frecuencia (% samp_rate)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_error_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._epsilon_range = Range(1-1e-4, 1+1e-4, 1e-6, 1, 200)
        self._epsilon_win = RangeWidget(self._epsilon_range, self.set_epsilon, 'Error de muestreo (% samp_rate)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._epsilon_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._d_range = Range(0, samp_per_sym-1, 1, 0, 200)
        self._d_win = RangeWidget(self._d_range, self.set_d, 'Muestra', "counter_slider", int)
        self.top_grid_layout.addWidget(self._d_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_2.addWidget(self._qtgui_const_sink_x_0_win)
        self.pfb_interpolator_ccf_0 = pfb.interpolator_ccf(
            samp_per_sym,
            pulso_srrc,
            100)
        self.pfb_interpolator_ccf_0.declare_sample_delay(0)
        self.isdbt_time_interleaver_0 = isdbt.time_interleaver(3, 13, 2, 0, 0, 0, 0)
        self.isdbt_time_deinterleaver_0 = isdbt.time_deinterleaver(3, 13, 2, 0, 0, 0, 0)
        self.isdbt_symbol_demapper_0 = isdbt.symbol_demapper(3, 13, 4, 0, 4, 0, 4)
        self.isdbt_hierarchical_combinator_0 = isdbt.hierarchical_combinator(3, 13, 0, 0)
        self.isdbt_frequency_interleaver_0 = isdbt.frequency_interleaver(False, 3)
        self.isdbt_frequency_deinterleaver_0 = isdbt.frequency_deinterleaver(False, 3)
        self.isdbt_energy_dispersal_0 = isdbt.energy_dispersal(3, 4, 0, 13)
        self.isdbt_energy_descrambler_0 = isdbt.energy_descrambler()
        self.isdbt_carrier_modulation_0 = isdbt.carrier_modulation(3, 13, 4)
        self.isdbt_byte_interleaver_0 = isdbt.byte_interleaver(3, 4, 0, 13)
        self.isdbt_byte_deinterleaver_0 = isdbt.byte_deinterleaver()
        self.isdbt_bit_deinterleaver_0 = isdbt.bit_deinterleaver(3, 13, 4)
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(1, pulso_srrc)
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.dtv_dvbt_viterbi_decoder_0 = dtv.dvbt_viterbi_decoder(dtv.MOD_QPSK, dtv.ALPHA4, dtv.C1_2, 204)
        self.dtv_dvbt_reed_solomon_enc_0 = dtv.dvbt_reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, 1)
        self.dtv_dvbt_reed_solomon_dec_0 = dtv.dvbt_reed_solomon_dec(2, 8, 0x11d, 255, 239, 8, 51, 1)
        self.dtv_dvbt_inner_coder_0_0 = dtv.dvbt_inner_coder(1, 1512*4, dtv.MOD_QPSK, dtv.ALPHA4, dtv.C1_2)
        self.channels_phase_noise_gen_0 = channels.phase_noise_gen(phase_noise, 0.01)
        self.channels_distortion_3_gen_0 = channels.distortion_3_gen(-0.11/10**(iip3/10.0))
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise,
            frequency_offset=freq_error,
            epsilon=epsilon,
            taps=[1],
            noise_seed=0,
            block_tags=False)
        self.blocks_vector_to_stream_2 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, data_carriers)
        self.blocks_vector_to_stream_0_1 = blocks.vector_to_stream(gr.sizeof_char*1, 1512*4)
        self.blocks_vector_to_stream_0_0_0 = blocks.vector_to_stream(gr.sizeof_char*1, 188)
        self.blocks_vector_source_x_0_0_0 = blocks.vector_source_c([0]*204*data_carriers, True, data_carriers, [gr.tag_utils.python_to_tag( [0, pmt.intern("frame_begin"), pmt.from_long(0), "yo"])])
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, throttle_rate,True)
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, data_carriers)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, 188)
        self.blocks_skiphead_1 = blocks.skiphead(gr.sizeof_gr_complex*1, int(np.floor(len(pulso_srrc)/samp_per_sym/2.0))+int(np.floor(len(pulso_srrc)/samp_per_sym/2.0)))
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*data_carriers, 2)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, samp_per_sym)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/lingles/fing/gr-isdbt/layer_a.ts', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, 'result_layer_b.ts', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_delay_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 3)
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, d)
        self.blocks_add_xx_0_0_0 = blocks.add_vcc(data_carriers)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.isdbt_frequency_deinterleaver_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_skiphead_1, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_vector_to_stream_2, 0))
        self.connect((self.blocks_skiphead_1, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.dtv_dvbt_reed_solomon_enc_0, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.blocks_add_xx_0_0_0, 1))
        self.connect((self.blocks_throttle_0_0, 0), (self.channels_phase_noise_gen_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.qtgui_const_sink_x_1, 0))
        self.connect((self.blocks_vector_source_x_0_0_0, 0), (self.blocks_add_xx_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1, 0), (self.isdbt_carrier_modulation_0, 0))
        self.connect((self.blocks_vector_to_stream_2, 0), (self.pfb_interpolator_ccf_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_delay_0_0_0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.channels_distortion_3_gen_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.channels_phase_noise_gen_0, 0), (self.channels_distortion_3_gen_0, 0))
        self.connect((self.dtv_dvbt_inner_coder_0_0, 0), (self.blocks_vector_to_stream_0_1, 0))
        self.connect((self.dtv_dvbt_reed_solomon_dec_0, 0), (self.blocks_vector_to_stream_0_0_0, 0))
        self.connect((self.dtv_dvbt_reed_solomon_enc_0, 0), (self.isdbt_energy_dispersal_0, 0))
        self.connect((self.dtv_dvbt_viterbi_decoder_0, 0), (self.isdbt_byte_deinterleaver_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.isdbt_bit_deinterleaver_0, 0), (self.dtv_dvbt_viterbi_decoder_0, 0))
        self.connect((self.isdbt_byte_deinterleaver_0, 0), (self.isdbt_energy_descrambler_0, 0))
        self.connect((self.isdbt_byte_interleaver_0, 0), (self.dtv_dvbt_inner_coder_0_0, 0))
        self.connect((self.isdbt_carrier_modulation_0, 0), (self.isdbt_hierarchical_combinator_0, 0))
        self.connect((self.isdbt_energy_descrambler_0, 0), (self.dtv_dvbt_reed_solomon_dec_0, 0))
        self.connect((self.isdbt_energy_dispersal_0, 0), (self.isdbt_byte_interleaver_0, 0))
        self.connect((self.isdbt_frequency_deinterleaver_0, 0), (self.isdbt_time_deinterleaver_0, 0))
        self.connect((self.isdbt_frequency_interleaver_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.isdbt_hierarchical_combinator_0, 0), (self.isdbt_time_interleaver_0, 0))
        self.connect((self.isdbt_symbol_demapper_0, 0), (self.isdbt_bit_deinterleaver_0, 0))
        self.connect((self.isdbt_time_deinterleaver_0, 0), (self.isdbt_symbol_demapper_0, 0))
        self.connect((self.isdbt_time_interleaver_0, 0), (self.isdbt_frequency_interleaver_0, 0))
        self.connect((self.pfb_interpolator_ccf_0, 0), (self.blocks_throttle_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "qpsk_transceiver_isdbt")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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
        self.set_sym_rate(self.samp_rate_estandar*self.data_carriers/((1+self.guard)*self.total_carriers))

    def get_samp_rate_estandar(self):
        return self.samp_rate_estandar

    def set_samp_rate_estandar(self, samp_rate_estandar):
        self.samp_rate_estandar = samp_rate_estandar
        self.set_sym_rate(self.samp_rate_estandar*self.data_carriers/((1+self.guard)*self.total_carriers))

    def get_guard(self):
        return self.guard

    def set_guard(self, guard):
        self.guard = guard
        self.set_sym_rate(self.samp_rate_estandar*self.data_carriers/((1+self.guard)*self.total_carriers))

    def get_data_carriers(self):
        return self.data_carriers

    def set_data_carriers(self, data_carriers):
        self.data_carriers = data_carriers
        self.set_sym_rate(self.samp_rate_estandar*self.data_carriers/((1+self.guard)*self.total_carriers))
        self.blocks_vector_source_x_0_0_0.set_data([0]*204*self.data_carriers, [gr.tag_utils.python_to_tag( [0, pmt.intern("frame_begin"), pmt.from_long(0), "yo"])])

    def get_sym_rate(self):
        return self.sym_rate

    def set_sym_rate(self, sym_rate):
        self.sym_rate = sym_rate
        self.set_samp_rate(self.sym_rate*self.samp_per_sym)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_pulso_srrc(firdes.root_raised_cosine(np.sqrt(self.samp_per_sym),self.samp_rate,self.samp_rate/self.samp_per_sym,self.alfa,self.len_sym_srrc*self.samp_per_sym))
        self.set_samp_rate(self.sym_rate*self.samp_per_sym)
        self.blocks_keep_one_in_n_0.set_n(self.samp_per_sym)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_pulso_srrc(firdes.root_raised_cosine(np.sqrt(self.samp_per_sym),self.samp_rate,self.samp_rate/self.samp_per_sym,self.alfa,self.len_sym_srrc*self.samp_per_sym))
        self.set_throttle_rate(self.samp_rate/1.0)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_len_sym_srrc(self):
        return self.len_sym_srrc

    def set_len_sym_srrc(self, len_sym_srrc):
        self.len_sym_srrc = len_sym_srrc
        self.set_pulso_srrc(firdes.root_raised_cosine(np.sqrt(self.samp_per_sym),self.samp_rate,self.samp_rate/self.samp_per_sym,self.alfa,self.len_sym_srrc*self.samp_per_sym))

    def get_alfa(self):
        return self.alfa

    def set_alfa(self, alfa):
        self.alfa = alfa
        self.set_pulso_srrc(firdes.root_raised_cosine(np.sqrt(self.samp_per_sym),self.samp_rate,self.samp_rate/self.samp_per_sym,self.alfa,self.len_sym_srrc*self.samp_per_sym))

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

    def get_pulso_srrc(self):
        return self.pulso_srrc

    def set_pulso_srrc(self, pulso_srrc):
        self.pulso_srrc = pulso_srrc
        self.fir_filter_xxx_0.set_taps(self.pulso_srrc)
        self.pfb_interpolator_ccf_0.set_taps(self.pulso_srrc)

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

    def get_d(self):
        return self.d

    def set_d(self, d):
        self.d = d
        self.blocks_delay_0_0_0.set_dly(self.d)

    def get_const_size(self):
        return self.const_size

    def set_const_size(self, const_size):
        self.const_size = const_size

    def get_active_carriers(self):
        return self.active_carriers

    def set_active_carriers(self, active_carriers):
        self.active_carriers = active_carriers



def main(top_block_cls=qpsk_transceiver_isdbt, options=None):
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
