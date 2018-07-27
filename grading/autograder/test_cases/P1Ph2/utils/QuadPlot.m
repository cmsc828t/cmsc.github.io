classdef QuadPlot < handle
    %QUADPLOT Visualization class for quad
    
    properties (SetAccess = public)
        k = 0;
        qn;             % quad number
        time = 0;       % time
        state;          % state
        des_state;      % desried state [x; y; z; xdot; ydot; zdot];
        rot;            % rotation matrix body to world
        
        wingspan;       % wingspan
        height;         % height of quad
        motor;          % motor position
        
        state_hist        % position history
        state_des_hist;   % desired position history
        time_hist;      % time history
        max_iter;       % max iteration
    end
   
    methods
        % Constructor
        function Q = QuadPlot(qn, state, wingspan, height, max_iter)
            Q.qn = qn;
            Q.state = state;
            Q.wingspan = wingspan;
            Q.height = height;
            Q.rot = QuatToRot(Q.state(7:10));
            Q.motor = quad_pos(Q.state(1:3), Q.rot, Q.wingspan, Q.height);
            Q.des_state = Q.state(1:6);
            
            Q.max_iter = max_iter;
            Q.state_hist = zeros(6, max_iter);
            Q.state_des_hist = zeros(6, max_iter);
            Q.time_hist = zeros(1, max_iter);
        end
        
        % Update quad state
        function UpdateQuadState(Q, state, time)
            Q.state = state;
            Q.time = time;
            Q.rot = QuatToRot(state(7:10))'; % Q.rot needs to be body-to-world
        end
        
        % Update desired quad state
        function UpdateDesiredQuadState(Q, des_state)
            Q.des_state = des_state;
        end
        
        % Update quad history
        function UpdateQuadHist(Q)
            Q.k = Q.k + 1;
            Q.time_hist(Q.k) = Q.time;
            Q.state_hist(:,Q.k) = Q.state(1:6);
            Q.state_des_hist(:,Q.k) = Q.des_state(1:6);
        end
        
        % Update motor position
        function UpdateMotorPos(Q)
            Q.motor = quad_pos(Q.state(1:3), Q.rot, Q.wingspan, Q.height);
        end
        
        % Truncate history
        function TruncateHist(Q)
            Q.time_hist = Q.time_hist(1:Q.k);
            Q.state_hist = Q.state_hist(:, 1:Q.k);
            Q.state_des_hist = Q.state_des_hist(:, 1:Q.k);
        end
        
        % Update quad plot
        function UpdateQuadPlot(Q, state, des_state, time)
            Q.UpdateQuadState(state, time);
            Q.UpdateDesiredQuadState(des_state);
            Q.UpdateQuadHist();
            Q.UpdateMotorPos();
        end
    end
    
end
