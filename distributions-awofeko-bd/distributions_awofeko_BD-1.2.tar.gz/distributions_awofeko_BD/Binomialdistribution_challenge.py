# TODO: import necessary libraries
import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution


# TODO: make a Binomial class that inherits from the Distribution class. Use the specifications below.
class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) epresenting the probability of an event occurring
    """

    #       A binomial distribution is defined by two variables:
    #           the probability of getting a positive outcome
    #           the number of trials

    #       If you know these two values, you can calculate the mean and the standard deviation
    #
    #       For example, if you flip a fair coin 25 times, p = 0.5 and n = 25
    #       You can then calculate the mean and standard deviation with the following formula:
    #           mean = p * n
    #           standard deviation = sqrt(n * p * (1 - p))

    #       

    # TODO: define the init function

    # TODO: store the probability of the distribution in an instance variable p
    # TODO: store the size of the distribution in an instance variable n

    def __init__(self, p=.5, size=20):

        self.n = size
        self.p = p

        Distribution.__init__(self, self.calculate_mean, self.calculate_stdev())

        # TODO: Now that you know p and n, you can calculate the mean and standard deviation You can use the
        #  calculate_mean() and calculate_stdev() methods defined below along with the __init__ function from the
        #  Distribution class

        # TODO: write a method calculate_mean() according to the specifications below

        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """

    @property
    def calculate_mean(self):

        self.mean = self.p * self.n

        return self.mean

        # TODO: write a calculate_stdev() method accordin to the specifications below.

    """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """

    def calculate_stdev(self):
        # standard deviation = sqrt(n * p * (1 - p))

        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))

        return self.stdev

    # TODO: write a replace_stats_with_data() method according to the specifications below. The read_data_file() from
    #  the Generaldistribution class can read in a data file. Because the Binomaildistribution class inherits from
    #  the Generaldistribution class, you don't need to re-write this method. However,  the method doesn't update the
    #  mean or standard deviation of a distribution. Hence you are going to write a method that calculates n, p,
    #  mean and standard deviation from a data set and then updates the n, p, mean and stdev attributes. Assume that
    #  the data is a list of zeros and ones like [0 1 0 1 1 0 1].
    #
    #       Write code that: 
    #           updates the n attribute of the binomial distribution
    #           updates the p value of the binomial distribution by calculating the
    #               number of positive trials divided by the total trials
    #           updates the mean attribute
    #           updates the standard deviation attribute
    #
    #       Hint: You can use the calculate_mean() and calculate_stdev() methods
    #           defined previously.

    def replace_stats_with_data(self):

        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """
        self.n = len(self.data)

        self.p = len([i for i in self.data if i == 1]) / len(self.data)

        self.mean = self.calculate_mean

        self.stdev = self.calculate_stdev()

        return self.p, self.n

    # TODO: write a method plot_bar() that outputs a bar chart of the data set according to the following
    #  specifications.
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        x_axis_one = 1
        y_axis_one = len([i for i in self.data if i == 1])
        x_axis_zero = 0
        y_axis_zero = len([i for i in self.data if i == 0])

        x = [x_axis_one, x_axis_zero]
        y = [y_axis_one, y_axis_zero]

        plt.bar(x, y)
        plt.title("EVENTS DISTRIBUTIONS")
        plt.xlabel("EVENTS")
        plt.ylabel("EVENTS FREQUNCES ")
        plt.show()

    # TODO: Calculate the probability density function of the binomial distribution
    def pdf(self, k):

        """Probability density function calculator for the binomial distribution.
        
        Args:
            x (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        a = math.factorial(self.n) / (math.factorial(k) * (math.factorial(self.n - k)))
        b = (self.p ** k) * (1 - self.p) ** (self.n - k)

        return a * b

    # write a method to plot the probability density function of the binomial distribution

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution


        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """
        x = []
        y = []

        # calculate the x values to visualize
        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pdf(i))

        # TODO: Use a bar chart to plot the probability density function from
        # k = 0 to k = n

        #   Hint: You'll need to use the pdf() method defined above to calculate the
        #   density function for every value of k.

        #   Be sure to label the bar chart with a title, x label and y label

        #   This method should also return the x and y values used to make the chart
        #   The x and y values should be stored in separate lists

        plt.bar(x, y)
        plt.title('BAR CHART OF BINOMIAL DISTRIBUTION')
        plt.xlabel('PROBABILITY COUNT')
        plt.ylabel('PROBABILITY OCCURENCE')
        plt.show()

    # write a method to output the sum of two binomial distributions_awofeko_BD. Assume both distributions_awofeko_BD have the same p value.
    def __add__(self, other):

        """Function to add together two Binomial distributions_awofeko_BD with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """

        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        # TODO: Define addition for two binomial distributions_awofeko_BD. Assume that the
        # p values of the two distributions_awofeko_BD are the same. The formula for
        # summing two binomial distributions_awofeko_BD with different p values is more complicated,
        # so you are only expected to implement the case for two distributions_awofeko_BD with equal p.

        # the try, except statement above will raise an exception if the p values are not equal

        # Hint: When adding two binomial distributions_awofeko_BD, the p value remains the same
        #   The new n value is the sum of the n values of the two distributions_awofeko_BD.

        resultes = Binomial()
        resultes.n = self.n + other.n
        resultes.p = self.p
        resultes.calculate_mean()
        resultes.calculate_stdev()

        return resultes

    def __repr__(self):

        # use the __repr__ magic method to output the characteristics of the binomial distribution object.

        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial object
        
        """
        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
        # TODO: Define the representation method so that the output looks like
        #       mean 5, standard deviation 4.5, p .8, n 20
        #
        #       with the values replaced by whatever the actual distributions_awofeko_BD values are
        #       The method should return a string in the expected format

        pass
