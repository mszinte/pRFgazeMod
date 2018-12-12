%% General experimenter launcher
%  =============================
% By :      Martin SZINTE
% Projet :  pRF_gazeMod experiment
% With :    Daniel LUTSCHER, Jan THEEUWES & Tomas KNAPEN
% Version:  4.0

% Version description
% ===================
% Experiment in which we first used a full screen 4 direction (left/right/up/down)
% bar pass stimuli in a attetion to fixation or attention to the bar experiment.
% Next, we use the same task but this time using a bar pass restricted to an aperture and 
% displayed at 3 different position surrounding the fixation target put at the screen center 
% or displaced to the left or to the right.

% TO DO
% =====
% code analysis of behavioral data
% code eye and data analysis with python started by terminal instructions

% First settings
% --------------
Screen('CloseAll');clear all;clear mex;clear functions;close all;home;ListenChar(1);AssertOpenGL;

% General settings
% ----------------
const.expName           =   'pRFgazeMod';   % experiment name.
const.expStart          =   0;              % Start of a recording exp                          0 = NO  , 1 = YES
const.checkTrial        =   0;              % Print trial conditions (for debugging)            0 = NO  , 1 = YES
const.writeLogTxt       =   1;              % write a log file in addition to eyelink file      0 = NO  , 1 = YES
const.genStimuli        =   1;              % Generate all stimuli                              0 = NO  , 1 = YES
const.drawStimuli       =   0;              % Draw stimuli generated                            0 = NO  , 1 = YES
const.mkVideo           =   0;              % Make a video of a run (on mac not linux)          0 = NO  , 1 = YES

% External controls
% -----------------
const.tracker           =   0;              % run with eye tracker                              0 = NO  , 1 = YES
const.scanner           =   0;              % run in MRI scanner                                0 = NO  , 1 = YES
const.scannerTest       =   1;              % run with T returned at TR time                    0 = NO  , 1 = YES

% Durations
% ---------
% AttendFixGazeCenterFS:  4 x 3.0 min ~ 12 min (each run: 154 TR of 3.1 min)
% AttendFixGazeCenter:    2 x 2.5 min ~ 05 min (each run: 126 TR of 1.2 min)
% AttendFixGazeLeft:      2 x 3.5 min ~ 05 min (each run: 126 TR of 1.2 min)
% AttendFixGazeRight:     2 x 3.5 min ~ 05 min (each run: 126 TR of 1.2 min)

% AttendStimGazeCenter:   4 x 4.1 min ~ 12 min (each run: 154 TR of 3.1 min)
% AttendStimGazeCenter:   2 x 3.5 min ~ 05 min (each run: 126 TR of 1.2 min)
% AttendStimGazeLeft:     2 x 3.5 min ~ 05 min (each run: 126 TR of 1.2 min)
% AttendStimGazeRight:    2 x 3.5 min ~ 05 min (each run: 126 TR of 1.2 min)
%                                       ------
% Total                               ~ 54 min

% Run order
% ---------
const.cond_run_order    =  [1,4;2,4;...     %    run 01 - AttendFixGazeCenterFS_run1  | run 02 - AttendStimGazeCenterFS_run1 |  L1+R1+U1+D1
                            1,4;2,4;...     %    run 03 - AttendFixGazeCenterFS_run2  | run 04 - AttendStimGazeCenterFS_run2 |  L2+R2+U2+D2
                            1,1;2,1;...     %    run 05 - AttendFixGazeLeft_run1      | run 06 - AttendStimGazeLeft_run1     |  L2+R2
                            1,3;2,3;...     %    run 07 - AttendFixGazeRight_run1     | run 08 - AttendStimGazeRight_run1    |  L2+R2
                            1,2;2,2;...     %    run 09 - AttendFixGazeCenter_run1    | run 10 - AttendStimGazeCenter_run1   |  L2+R2
                            ...
                            1,4;2,4;...     %    run 11 - AttendFixGazeCenterFS_run3  | run 12 - AttendStimGazeCenterFS_run3 |  L3+R3+U3+D3
                            1,4;2,4;...     %    run 13 - AttendFixGazeCenterFS_run4  | run 14 - AttendStimGazeCenterFS_run4 |  L4+R4+U4+D4
                            1,1;2,1;...     %    run 15 - AttendFixGazeLeft_run2      | run 16 - AttendStimGazeLeft_run2     |  L4+R4
                            1,3;2,3;...     %    run 17 - AttendFixGazeRight_run2     | run 18 - AttendStimGazeRight_run2    |  L4+R4
                            1,2;2,2];       %    run 19 - AttendFixGazeCenter_run2    | run 20 - AttendStimGazeCenter_run2   |  L4+R4
                            
% Run number per condition
% ------------------------
const.cond_run_num      =  [1;1;...
                            2;2;...
                            1;1;...
                            1;1;...
                            1;1;...
                            3;3;...
                            4;4;...
                            2;2;...
                            2;2;...
                            2;2;];

% Desired screen setting
% ----------------------
const.desiredFD         =   120;            % Desired refresh rate
% fprintf(1,'\n\n\tDon''t forget to change before testing\n');
const.desiredRes        =   [1920,1080];    % Desired resolution

% Path
% ----
dir                     =   (which('expLauncher'));
cd(dir(1:end-18));

% Add Matlab path
% ---------------
addpath('config','main','conversion','eyeTracking','instructions','trials','stim');

% Subject configuration
% ---------------------
[const]                 =   sbjConfig(const);
                        
% Main run:
% ---------
main(const);