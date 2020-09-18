import matplotlib.pyplot as plt

class SpymPlotting():
    ''' Plotting.
    
    '''

    def __init__(self, spym_instance):
        self._spym = spym_instance

    def plot(self, title=None, **kwargs):
        ''' Plot data with custom parameters.

        Args:
            title: title of the figure (string). By default gives some basic information on the data plotted. Pass an empty string to disable it.
            **kwargs: any argument accepted by xarray.plot() function.

        '''

        dr = self._spym._dr

        # Create figure
        # xarray plot() wraps:
        #   - matplotlib.pyplot.plot() for 1d arrays
        #   - matplotlib.pyplot.pcolormesh() for 2d arrays
        #   - matplotlib.pyplot.hist() for anything else
        plot = dr.plot()

        # Set figure title
        if title is None:
            title = self.format_title()
        plt.title(title)

        # Set images properties (2d arrays)
        # plot is an instance of matplotlib.collections.QuadMesh
        if dr.data.ndim == 2 and not isinstance(plot, list):
            fig = plot.get_figure()
            ax = plot.axes
            # Fit figure pixel size to image
            fig_width, fig_height = self.fit_figure_to_image(fig, dr.data, ax)
            fig.set_size_inches(fig_width, fig_height)

            # Apply colormap
            plot.set_cmap('afmhot')

        plt.draw()

    def format_title(self):
        ''' Provide a title from the metadata of the DataArray.

        '''

        title = ""
        attrs = self._spym._dr.attrs

        if "filename" in attrs:
            title += attrs["filename"] + "\n"

        title += "{:.2f} {}, {:.2f} {}".format(
            attrs["bias"],
            attrs["bias_units"],
            attrs["setpoint"],
            attrs["setpoint_units"])

        return title

    def fit_figure_to_image(self, figure, image, axis=None):
        ''' Calculate figure size so that plot (matplotlib axis) pixel size is equal to the image size.

        Args:
            figure: matplotlib Figure instance.
            image: 2d numpy array.
            axis: axis of the figure to adapt, if None takes the first (or only) axis.

        Returns:
            adapted width and height of the figure in inches.

        '''

        if axis is None:
            axis = figure.axes[0]
        bounds = axis.bbox.bounds

        im_width, im_height = image.shape

        width_scale = im_width/bounds[2]
        height_scale = im_height/bounds[3]

        fig_width, fig_height = figure.get_size_inches()

        return fig_width*width_scale, fig_height*height_scale
