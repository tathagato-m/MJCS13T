import numpy as np
from matplotlib import pyplot as plt
from sys import argv
from enum import IntEnum
import re

SAMPLE_RATE = 200000  # Hertz
BIT_RATE = 1000 #bits/sec
FREQ = 2000 #Hertz 
class MOD_type(IntEnum):
  QPSK = 0
  PSK_8 = 1
  PSK_16 = 2

def generate_sine_wave(x, start_t, duration, amp, freq, phase):
    y = amp * np.cos((2 * np.pi) * freq * x[start_t:start_t+duration-1] + phase)
    return y

def m_ary_psk(mod_type, bs) :
  symb = [["00","01","11","10"],["000","001","011","010","110","111","101","100"],["0000","0001","0011","0010","0110","0111","0101","0100","1000","1001","1011","1010","1110","1111","1101","1100"]]
  phase = [[np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4],[np.pi/8, 3*np.pi/8, 5*np.pi/8, 7*np.pi/8, 9*np.pi/8, 11*np.pi/8, 13*np.pi/8, 15*np.pi/8],[np.pi/16, 3*np.pi/16, 5*np.pi/16, 7*np.pi/16, 9*np.pi/16, 11*np.pi/16, 13*np.pi/16, 15*np.pi/16,17*np.pi/16, 19*np.pi/16, 21*np.pi/16, 23*np.pi/16, 25*np.pi/16, 27*np.pi/16, 29*np.pi/16, 31*np.pi/16]]
  bits_per_sample = [2,3,4]
  mod_t = MOD_type[mod_type] 
  l = len(bs)
  num_symb = int(l/bits_per_sample[mod_t])
  duration = float(l)/BIT_RATE
  samples_per_symb = int(SAMPLE_RATE/BIT_RATE*bits_per_sample[mod_t])
  total_samples = num_symb * samples_per_symb
  x = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=True)
  y = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=True)
  symbol_idx = 0
  for i in range(0,l,bits_per_sample[mod_t]) :
    for j in range(len(symb[mod_t])):
      if re.search("\A"+symb[mod_t][j],bs[i:]) != None :
        print(phase[mod_t][j])
        y[symbol_idx*samples_per_symb: (symbol_idx+1)*samples_per_symb-1] = generate_sine_wave(x, symbol_idx*samples_per_symb, samples_per_symb, 1.0, FREQ, phase[mod_t][j])
    symbol_idx = symbol_idx + 1
   
  return x, y


if __name__=='__main__':
  x, y = m_ary_psk(argv[1], argv[2])
  fig=plt.figure()
  ax=fig.add_subplot(1,1,1)
  l = ax.plot(x, y)
  plot_dur = float(len(argv[2]))/float(BIT_RATE)
  ax.set_xticks(np.arange(0,plot_dur, 1.0/FREQ))
  ax.set_xticks(np.arange(0,plot_dur, 1.0/FREQ), minor=True)
  ax.set_yticks(np.arange(-1.5,1.5, 0.5))
  ax.set_yticks(np.arange(-1.5,1.5, 0.1), minor=True)
  for tick in ax.get_xticklabels():
    tick.set_rotation(90)
  ax.grid(True)

  plt.show()
  fig.set_size_inches(8,5)
  fig.savefig('test.png',dpi=100)
       
