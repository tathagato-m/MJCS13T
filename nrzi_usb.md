# NRZ-I and USB 

## USB signal basics

USB (Full-Speed 12 Mbps, Low-Speed 1.5 Mbps) is transmitted over two differential data lines: D+ and D−.

Logical 1 and 0 are not represented directly as high/low voltages, but as changes or no changes in the signal level.

## NRZ-I Encoding Rule 

Logical 1 → no change in signal level. <br />
Logical 0 → toggle (invert) the signal level. <br />
This helps in avoiding too many transitions for consecutive 1’s, which makes it more bandwidth-efficient than simple NRZ. <br />

The figure below shows an illustration of transmitted signal and received signal in presence of moderate noise of an inverted NRZ-I coding (i.e no change in level for logical 0 and change in level for logical 1).

<figure>
<img src=/home/tathagato/classes/2025_26/digicomm/LineCoding/nrz_i_with_low_noise.png alt="NRZ-I Tx and Rx waveform">
<figcaption><center>Inverted NRZ-I transmitted and received signal with noise</center></figcaption>
</p>
</figure>

## Problem and one possible solution

As logical 1's do not trigger any transitions, a bitstream having a long run of 1's results in absence of transitions during all those bit periods. This might result in loss of clock synchronization in the receiver as the receiver keeps synchronization of its bit interval clock with the transitions themselves.

### A possible solution : Bit stuffing

One possible solution to break the long absence of transitions is deliberate insertion of a 0 after a particular number of consecutive 1's (say 6). This introduces a transition forcibly. In the receiver, the first 0 after 6 consecutive 1's needs to be expunged as "not being part of the data". This scheme is used for USB2.0 for 1.5Mbps or 12 Mbps speeds. For 480 Mbps and beyond, this scheme is not used as the receiver needs to keep the past 6 received bits - and bit errors can actually percolate. 

## Other solutions

Other techniques employed in the high-speed USB link employs different solutions than bit-stuffing.

### USB2.0 High Speed (480 Mbps)

In addition to NRZI and bit-stuffing, another technique called scrambling is used. Scrambling is actually a procedure where each output bit is a function of last few input bits - input bits stored in a shift register and are shifted by 1 position with each bit clock. For example, one 16-bit scrambling function can be as follows (let $b_i$ be the input bit and $b_{i-n}$ is the $n^{th}$ previous bit) : <br />
$x_i$ = $b_i + b_{i-6} + b_{i-7}$. Initially all stages of the shift register can be initialized to 1. 


### USB3.0/3.1 Gen 1 

The approach taken for avoiding long stream of 1's is similar to that of USB 2.0, with differences that :
- bit stuffing not used,
- the scrambling function is $x_i = b_i + b_{i-2} + b_{i-3} + b_{i-4} + b_{i-5} + b_{i-15}$ using a 16-bit shift register,
- 8b/10b encoding is used after scrambling.

After this scrambling, 8b/10b encoding is applied to generate the final output. The 8b/10b encoding involves generation of a 10-bit sequence from the input 8-bit sequence based on a lookup table depending on difference of 1's and 0's in the 5 LSBs and 3 MSBs and the cumulative difference of 1's and 0's clipped to at 
most 1. These two steps avoid occurences of consecutive 1's.

#### 8b/10b encoding

This encoding is illustrated with an example below. <br />
Let the byte to transmit be 10011011 01001010 00010111. <br />

Sequences are split into 3-bit MSB's and 5-bit LSBs and written into 5bit.3bit value notation. So 10011011 becomes 11011.100 or 27.4, 01001010 becomes 10.2, 00010111 becomes 23.0. <br />

According to the lookup table for 8b/10b encoding : <br />
11011 is mapped to two values 110110 and 001001 for cases where recurring disparity is -ve or +ve. Recurring disparity is the sign of cumulative (number of 1s - number of 0's) transmitted so far. <br />
Let the initial disparity be assumed to be -ve. Then the mapped value 110110 is considered for input 11011. The mapped code 110110 has disparity D = +2. Hence, initial disparity is -ve, disparity for the 6-bit code = +2, current D after the 6-bit code = +ve. <br /> 
Now, the next 3-bit 100 - which can be mapped to 0010 or 1101 - now if 0010 is used, the D value would be -2, which would balance the D value of the previous 6-bit code. Hence, for the 8-bit value 10011011, transmitted 10-bit value would be  would be  1101100010 the 10 bit code transmitted. The D value for the entire codeword = 5-5 = 0, which does not alter the initial D value. <br />
An important point to note here is that, any 10bit codeword would have the D value of either +2, -2 or 0. If initial D is -ve, codeword D = +2, resultant D = -ve. For -ve initial D, codeword with D = -2 would not be chosen. This is how the DC balance is maintained. <br />
The table is called Widmer–Franaszek mapping table. <br />
Similarly, the rest of the bytes are encoded. 
    
### USB3.1 Gen 2 (data rates 10 Gbps or higher) 

The following steps are followed :

- The 128-bit payload is scrambled with a self-synchronous scrambler with 24-bit shift register. Each input bit $x_i$ is XOR'ed to $y_i$, which is  $y_{i-23}$ XOR $y_{i-16}$ XOR $y_{i-8}$ XOR $y_{i-5}$ XOR $y_{i-2}$. The resultant output $x_i$ XOR $y_i$ is transmitted as well as pushed in the shift register from the LSB onwards. Initial state before any transmission : 1 in all shift register stages. This scrambling is different than the 8-bit or 16-bit scrambling employed earlier. In earlier cases, the shift register starts from an initial position for each frame, and contains earlier input bits. Whereas here, the shift register contains the last transmitted bits - and the shift register is not reset after each frame.  
- Instead of 8b/10b encoding, a 128b/132b encoding is used, where a 4-bit sync header 0010 (for data block) and 1101 (Control block) is prepended to 128-bit data block. 
- The 4-bit header is chosen such that it cannot occur within the scrambled 128-bit payload.

This scrambling scheme is expected to statistically balance the number of 1's  and 0's - hence no other bit-stuffing or 8b/10b encoding is necessary. The receiver also is expected to maintain a shift register in the same way as the transmitter, and the shift register state after one 128-bit block is retained for the next 128-bit block.
