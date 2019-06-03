clear;close all;
%输入原始数据
pupil_x = [307, 270, 236; 
                    305, 266, 229;
                    301, 262, 225];
pupil_y = [152, 150, 153;
                    169, 167, 173;
                    197, 195, 198];
front_x = [263, 405, 553;
                    265, 405, 551;
                    266, 404, 552];
front_y = [104, 103, 101;
                    247, 246, 248;
                    386, 390, 394];
                
%使用x轴的列均值做回归方程；使用y轴的行均值做回归方程
pupil_x_mean = mean(pupil_x)';
pupil_y_mean = mean(pupil_y,2);
front_x_mean = mean(front_x)';
front_y_mean = mean(front_y,2);

%做回归分析
reg_para_x = polyfit(pupil_x_mean,front_x_mean,1);
reg_para_y = polyfit(pupil_y_mean,front_y_mean,1);

temp_y = pupil_x_mean * reg_para_x(1) + reg_para_x(2);
temp_x = pupil_y_mean * reg_para_y(1) + reg_para_y(2);

figure(1)
plot(pupil_x_mean,front_x_mean,pupil_x_mean,temp_y);
figure(2)
plot(pupil_y_mean,front_y_mean,pupil_y_mean,temp_x);

disp(strcat('xm = ',num2str(reg_para_x(1)),' * x + ' , num2str(reg_para_x(2))));
disp(strcat('ym = ',num2str(reg_para_y(1)),' * y + ' , num2str(reg_para_y(2))));