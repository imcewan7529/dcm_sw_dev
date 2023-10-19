

class Lowpass_Filter(object):
    K = 3
    N = int(1 << K)
    def __init__ (self):
        self.sum = 0
        self.buffer = [0] * Lowpass_Filter.N
        self.buffer_ptr = 0

    def Lowpass_Filter(self, input_voltage):
        self.sum -= self.buffer[self.buffer_ptr]
        self.buffer[self.buffer_ptr] = input_voltage
        self.sum += self.buffer[self.buffer_ptr]
        self.buffer_ptr += 1
        self.buffer_ptr %= Lowpass_Filter.N 
        #print( self.sum /8)
        return (self.sum/8)


