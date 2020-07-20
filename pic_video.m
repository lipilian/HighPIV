load('9HZ_high_crop.mat');

%%
writerObj = VideoWriter('9hz_test.avi');
writerObj.FrameRate = 2;
open(writerObj);
for i = 1:100
    h = figure(1);
    set(h,'Position',[100, 100, 800, 500])
    quiver(X,Y,Uall(:,i),Vall(:,i),2);
    axis([0 250 -70 10]);
    writeVideo(writerObj, getframe(h));
end

close(writerObj);
%%
U_mean = mean(Uall,2);
[m,n] = size(Uall);
Up = Uall;
for i = 1:n
    Up(:,i) = Uall(:,i) - U_mean;
end
Xc = (reshape(X,212,65));
Yc = (reshape(Y,212,65));

for i = 1:1899
    Uc = (reshape(Up(:,i),212,65));
    a = figure(2);
    [C,h] = contourf(Xc,Yc,Uc,100);
    set(h,'LineColor','none');
    colormap(redblue);
    caxis([-0.5 0.5]);
    hold on;
    quiver(X,Y,Uall(:,i),Vall(:,i),2,'color',[0,0,0]);
    hold off;
    axis([0 250 -70 10]);
    F(i) = getframe(a);
    i
end
%%
writerObj = VideoWriter('9hz_coutourf.avi');
writerObj.FrameRate = 25;
open(writerObj);
for i = 1:length(F)
    writeVideo(writerObj, F(i));
    i
end
close(writerObj);
%%
Uc = Up(:,100);
max(max(Uc))
min(min(Uc))
%%
%Uc = (reshape(Up(:,1),212,65));
%Uc_max = max(max(Uc));
%Uc_min = min(min(Uc));
%[C,h] = contourf(Xc,Yc,Uc,100);
%set(h,'LineColor','none')
%colormap(LiuHong_RedB);