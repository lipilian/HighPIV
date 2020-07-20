function [freq P1]=leo_spectra_detailed(u,nwin,f,smoothSize)

%close all

P=u;
Time=length(P)/f; 

np = f*Time/nwin;
uhat=P;
U=mean(uhat);
urms=sqrt(mean((uhat-U).^2));

deltaf=f/np;
uprim=uhat-U;
nset = floor(length(uprim)/np);
P1 = zeros(np/2,1);
for n=1:nset
                uslask = uprim((n-1)*np+1:n*np);
                E=fft(uslask)/np;
                Pslask = (abs(E)).^2; 
                P1 = P1 + 2*(Pslask(1:np/2));
end
P1 = P1/(nset);
P1=P1/(f/np);  
freq = (0:np/2-1) *f/np;%.*0.12./0.125;
freq = freq(1:np/2-1);
P1 = smooth(P1(1:np/2-1),smoothSize);
%P1 = smooth(P1(1:np/2-1),smoothSize);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%figure;
%loglog(freq(1:np/2-1),P1(1:np/2-1), 'b','Color',[0 0 0]);
%loglog(freq(1:np/2-1),smooth(freq(1:np/2-1)' .* P1(1:np/2-1),3), 'b','Color',[0 0 0]);
%loglog(freq(1:np/2-1),smooth(P1(1:np/2-1), 3), 'b','Color',[0 0 0]);
%loglog(freq(1:np/2-1), P1(1:np/2-1), 'b','Color',[0 0 0]);

%figure(1);
% axes('YScale','log','YMinorTick','on','XScale','log','XMinorTick','on','FontSize',14);
% set(gcf,'position',[300 100 560 470]);



%pre
%loglog(freq(1:np/2-1),smooth(freq(1:np/2-1)'.*P1(1:np/2-1)/var(P),8), 'b','Color',[0 0 0]);


%%%%%%%%%%%%%%%%%%%%%%%




end