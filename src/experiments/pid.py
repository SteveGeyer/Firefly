"""Basic PID algorithm.

This algorithm is based on:
  http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/

Any errors in the implementation are mine.
"""

__author__ = "Steve Geyer"
__copyright__ = "Copyright 2019, Steve Geyer"
__credits__ = ["Steve Geyer"]
__license__ = "BSD 3-Clause License"
__version__ = "1.0.0"
__status__ = "Development"

class PID:
    """Basic PID algorithm."""

    def __init__(self, forward):
        """Initialize PID with is core parameters."""
        self.forward = forward
        self.kp = 0.0
        self.ki = 0.0
        self.kd = 0.0
        self.p_on_e = False
        self.out_min = 0.0
        self.out_max = 0.0
        self.iterm = 0.0
        self.output = 0.0
        self.set_point = 0.0
        self.last_time = 0.0
        self.last_input = 0.0
        self.init_input = 0.0

    def set_output_limits(self, min_value, max_value):
        """Set output min and max."""
        self.out_min = min_value
        self.out_max = max_value
        if self.out_min > self.out_max:
            print("set_output_limits(): min must be smaller than max.")
        self.iterm = self.clip_to_output_limits(self.iterm)
        self.output = self.clip_to_output_limits(self.output)

    def set_tunings(self, kp, ki, kd, p_on_e):
        """Set the tuning parameters."""
        if kp < 0 or ki < 0 or kd < 0:
            print("PID parameters cannot be less than zero.")
        if self.forward:
            self.kp = kp
            self.ki = ki
            self.kd = kd
        else:
            self.kp = -kp
            self.ki = -ki
            self.kd = -kd
        self.p_on_e = p_on_e

    def set_set_point(self, set_point):
        """Set the set_point."""
        self.set_point = set_point

    def prep_for_start(self, now, input_value):
        """Call once before starting the controller to set
           time and input baseline."""
        self.last_time = now
        self.last_input = input_value
        self.init_input = input_value

    def compute(self, now, input_value):
        """Take time (in seconds) and current input value, update PID
           and return new control signal."""

        # Calculate time change. Return last output if no change.
        time_change = now - self.last_time
        if time_change <= 0:
            return self.output

        # Get and update constants.
        kp = self.kp
        ki = self.ki * time_change
        kd = self.kd / time_change

        # Compute all the working error variables.
        input_error = self.set_point - input_value
        self.iterm += (ki * input_error)
        self.iterm = self.clip_to_output_limits(self.iterm)
        d_input = input_value - self.last_input

        # Compute the P-Term.
        if self.p_on_e:
            self.output = kp * input_error
        else:
            self.output = -kp * (input_value-self.init_input)

        # Compute the rest of PID Output.
        self.output += self.iterm - kd * d_input
        self.output = self.clip_to_output_limits(self.output)

        # Remember state for next time.
        self.last_input = input_value
        self.last_time = now

        # Result value.
        return self.output

    def clip_to_output_limits(self, value):
        """Clip outputs to PID limits."""
        return max(self.out_min, min(self.out_max, value))
