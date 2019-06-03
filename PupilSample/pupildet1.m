% 检测瞳孔坐标
% 邓昭宇 10月27日
% 调整thresh会出现空矩阵情况
% thresh=0会出现检测到眼睑的BUG
clc; clear; close all;
% 图片分辨率: 480 x 640
resw = 480; resh = 640;
% 人工调节的瞳孔可能出现范围
ROIx = 100; ROIy = 120; ROIw = 350; ROIh = 240;
% 比较的最长线段最小阈值
maxLenThresh = 10;
for x = 9
    % 读取图片RGB矩阵
    eyeRGB = imread([num2str(x), '.jpg']);
    % 由于眼部摄像头已经设为灰度图，因此直接抽取一层
    eye = eyeRGB(:,:,1);
    % 设置阈值获得突出瞳孔的二值图
    eyeBin = eye < 30;
%     eyeBin = ~eyeBin; % 非运算,方便观察
%     figure('Name','Binary Image')
    % 图片显示:1白色,0黑色
%     imshow(eyeBin);
%     rectangle('position',[ROIx,ROIy,ROIw,ROIh],'EdgeColor','red');
    
    % 截取ROI矩阵（瞳孔可能出现范围）
    eyeROI = eyeBin( ROIy:ROIy+ROIh,ROIx:ROIx+ROIw);
    % 显示二值图
    figure('Name','ROI Binary Image');
    % 图片显示:true白色,false黑色
    imshow(eyeROI);
    
    % 扫描横向最长连续线段位置与长度
    % 初始化[y坐标,x起始坐标,长度]
    statH = zeros(ROIh,3);
    for h = 1:ROIh
        % 前一项为0标志位
        isFore0 = true;
        % 用作选择最大值的比较临时变量
        tmpMaxLen = maxLenThresh;
        for w = 1:ROIw
            if eyeROI(h,w) == true && isFore0 == true
                startX = w;
                 isFore0 = false;
            elseif eyeROI(h,w) == false && isFore0 == false
%                 endX = [h,w]; % 注意此点为false
                isFore0 = true;
                len = w - startX;
                if len > tmpMaxLen
                    % 比较最终获得此行最长线段
                    statH(h,:) = [h,startX,len];
                end;
            end;
        end;
    end;
    % 获得最长横线段
    [maxLenH,indexH] = max(statH(:,3));
    rectangle('position',[statH(indexH,2),statH(indexH,1),maxLenH,0],'EdgeColor','red');
    
    % 扫描纵向最长连续线段位置与长度
    scanStartX = statH(indexH,2);
    % 初始化[x坐标,y起始坐标,长度]
    statW = zeros(maxLenH,3);
    for w = 1:maxLenH
        % 前一项为0标志位
        isFore0 = true;
        % 用作选择最大值的比较临时变量
        tmpMaxLen = maxLenThresh;
        for h = 1:ROIh
            if eyeROI(h,w+scanStartX) == true && isFore0 == true
                startY = h;
                 isFore0 = false;
            elseif eyeROI(h,w+scanStartX) == false && isFore0 == false
%                 endX = [h,w]; % 注意此点为false
                isFore0 = true;
                len = h - startY;
                if len > tmpMaxLen
                    % 比较最终获得此行最长线段
                    statW(w,:) = [w,startY,len];
                end;
            end;
        end;
    end;
    % 获得最长纵线段
    [maxLenW,indexW] = max(statW(:,3));
    rectangle('position',[statW(indexW,1)+scanStartX,statW(indexW,2),0,maxLenW],'EdgeColor','red');
    
    % 获得横纵两线段中点综合坐标
    irisX = statH(indexH,2)+maxLenH/2;
    irisY = statW(indexW,2)+maxLenW/2;
    % 标出瞳孔中点
    crossSize = 40;
    rectangle('position',[irisX-crossSize/2,irisY,crossSize,0],'EdgeColor','blue');
    rectangle('position',[irisX,irisY-crossSize/2,0,crossSize],'EdgeColor','blue');
    
end;