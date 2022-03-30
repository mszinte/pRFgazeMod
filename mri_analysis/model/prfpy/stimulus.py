import numpy as np


class PRFStimulus2D(object):
#     """PRFStimulus2D

#     Minimal visual 2-dimensional pRF stimulus class, 
#     which takes an input design matrix and sets up its real-world dimensions.
#     """

#     def __init__(self,
#                  screen_width_cm,
#                  screen_height_cm,
#                  screen_distance_cm,
#                  design_matrix,
#                  TR,                 
#                  task_lengths=None,
#                  task_names=None,
#                  late_iso_dict=None, **kwargs):
#         """
        

#         Parameters
#         ----------
#         screen_width_cm : float
#             size of screen width in centimeters
#         screen_height_cm : float
#             size of screen height in centimeters
#         screen_distance_cm : float
#             eye-screen distance in centimeters
#         design_matrix : numpy.ndarray
#             an N by t matrix, where N is [x, x]. 
#             represents a square screen evolving over time (time is last dimension)
#         TR : float
#             Repetition time, in seconds
#         task_lengths : list of ints, optional
#             If there are multiple tasks, specify their lengths in TRs. The default is None.
#         task_names : list of str, optional
#             Task names. The default is None.
#         late_iso_dict : dict, optional 
#             Dictionary whose keys correspond to task_names. Entries are ndarrays
#             containing the TR indices used to compute the BOLD baseline for each task.
#             The default is None.


#         Raises
#         ------
#         ValueError
#             DESCRIPTION.

#         Returns
#         -------
#         None.
        
#         """

#         self.screen_width_cm = screen_width_cm
#         self.screen_height_cm = screen_height_cm
#         self.screen_distance_cm = screen_distance_cm
#         self.design_matrix = design_matrix
#         self.TR = TR
                
#         # other useful stimulus properties
#         self.task_lengths = task_lengths
#         self.task_names = task_names
#         self.late_iso_dict = late_iso_dict

#         self.screen_width_degrees = 2.0 * np.degrees(np.arctan(self.screen_width_cm /(2.0*self.screen_distance_cm)))
#         self.screen_height_degrees = 2.0 * np.degrees(np.arctan(self.screen_height_cm /(2.0*self.screen_distance_cm)))

# #         oneD_grid_column = np.linspace(-self.screen_width_degrees/2,
# #                                  self.screen_width_degrees/2,
# #                                  self.design_matrix.shape[0],
# #                                  endpoint=True)

# #         oneD_grid_row = np.linspace(-self.screen_height_degrees/2,
# #                                  self.screen_height_degrees/2,
# #                                  self.design_matrix.shape[1],
# #                                  endpoint=True)
# #         self.x_coordinates, self.y_coordinates = np.meshgrid(
# #             oneD_grid_row, oneD_grid_column)
        
        
#         oneD_grid_row = np.linspace(-self.screen_height_degrees/2,
#                                  self.screen_height_degrees/2,
#                                  self.design_matrix.shape[0],
#                                  endpoint=True)

#         oneD_grid_column = np.linspace(-self.screen_width_degrees/2,
#                                  self.screen_width_degrees/2,
#                                  self.design_matrix.shape[1],
#                                  endpoint=True)        
        
#         self.x_coordinates, self.y_coordinates = np.meshgrid(
#             oneD_grid_column, oneD_grid_row)
        
        
#         self.complex_coordinates = self.x_coordinates + self.y_coordinates * 1j
#         self.ecc_coordinates = np.abs(self.complex_coordinates)
#         self.polar_coordinates = np.angle(self.complex_coordinates)
#         self.max_ecc = np.max(self.ecc_coordinates)

#         # construct a standard mask based on standard deviation over time
#         self.mask = np.std(design_matrix, axis=-1) != 0

    def __init__(self,
                 screen_size_cm,
                 screen_distance_cm,
                 design_matrix,
                 TR,                 
                 task_lengths=None,
                 task_names=None,
                 late_iso_dict=None, **kwargs):
        """
        
        Parameters
        ----------
        screen_size_cm : float
            size of screen in centimeters
        screen_distance_cm : float
            eye-screen distance in centimeters
        design_matrix : numpy.ndarray
            an N by t matrix, where N is [x, x]. 
            represents a square screen evolving over time (time is last dimension)
        TR : float
            Repetition time, in seconds
        task_lengths : list of ints, optional
            If there are multiple tasks, specify their lengths in TRs. The default is None.
        task_names : list of str, optional
            Task names. The default is None.
        late_iso_dict : dict, optional 
            Dictionary whose keys correspond to task_names. Entries are ndarrays
            containing the TR indices used to compute the BOLD baseline for each task.
            The default is None.
        **kwargs : optional
            Use normalize_integral_dx = True to normalize the prf*stim sum as an integral.
        Raises
        ------
        ValueError
            DESCRIPTION.
        Returns
        -------
        None.
        """



        self.screen_size_cm = screen_size_cm
        self.screen_distance_cm = screen_distance_cm
        self.design_matrix = design_matrix
        if len(self.design_matrix.shape) >= 3 and self.design_matrix.shape[0] != self.design_matrix.shape[1]:
            raise ValueError  # need the screen to be square
        self.TR = TR

        
        # other useful stimulus properties
        self.task_lengths = task_lengths
        self.task_names = task_names
        self.late_iso_dict = late_iso_dict


        self.screen_size_degrees = 2.0 * \
            np.degrees(np.arctan(self.screen_size_cm /
                                 (2.0*self.screen_distance_cm)))

        oneD_grid = np.linspace(-self.screen_size_degrees/2,
                                self.screen_size_degrees/2,
                                self.design_matrix.shape[0],
                                endpoint=True)




        self.x_coordinates, self.y_coordinates = np.meshgrid(
            oneD_grid, oneD_grid)
        self.complex_coordinates = self.x_coordinates + self.y_coordinates * 1j
        self.ecc_coordinates = np.abs(self.complex_coordinates)
        self.polar_coordinates = np.angle(self.complex_coordinates)
        self.max_ecc = np.max(self.ecc_coordinates)

        # construct a standard mask based on standard deviation over time
        self.mask = np.std(design_matrix, axis=-1) != 0
        
        # whether or not to normalize the stimulus_through_prf as an integral, np.sum(prf*stim)*dx**2
        self.normalize_integral_dx = kwargs.pop('normalize_integral_dx', False)
        
        if self.normalize_integral_dx:
            self.dx = self.screen_size_degrees/self.design_matrix.shape[0]
        else:
            self.dx = 1



class PRFStimulus1D(object):
    """PRFStimulus1D

    Minimal visual 1-dimensional pRF stimulus class, 
    which takes an input design matrix and sets up its real-world dimensions.

    """

    def __init__(self,
                 design_matrix,
                 mapping,
                 TR,
                 task_lengths=None,
                 task_names=None,
                 late_iso_dict=None,
                 **kwargs):
        """__init__


        Parameters
        ----------
        design_matrix : numpy.ndarray
            a 2D matrix (M by t). 
            represents inputs in an encoding space evolving over time (time is last dimension)
        mapping : numpy.ndarray, np.float
            for each of the columns in design_matrix, the value in the encoding dimension
            for example, in a numerosity experiment these would be the numerosity of presented stimuli
        TR : float
            Repetition time, in seconds
        task_lengths : list of ints, optional
            If there are multiple tasks, specify their lengths in TRs. The default is None.
        task_names : list of str, optional
            Task names. The default is None.
        late_iso_dict : dict, optional 
            Dictionary whose keys correspond to task_names. Entries are ndarrays
            containing the TR indices used to compute the BOLD baseline for each task.
            The default is None.

        """
        self.design_matrix = design_matrix
        self.mapping = mapping
        self.TR = TR
        
        # other potentially useful stimulus properties
        self.task_lengths = task_lengths
        self.task_names = task_names
        self.late_iso_dict = late_iso_dict
