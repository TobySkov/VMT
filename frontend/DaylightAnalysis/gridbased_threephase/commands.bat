@echo off
SET RAYPATH=.;c:\radiance\lib
PATH=c:\radiance\bin;%PATH%
C:
cd C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT\frontend\DaylightAnalysis\gridbased_threephase

echo :: total sky matrix
c:\radiance\bin\gendaymtx -O0 -r 0.0 -m 1 -v sky/skymtx_vis_r1_0_061800_55.63_12.67_0.0_SkyMatrix.wea > sky/skymtx_vis_r1_0_061800_55.63_12.67_0.0_SkyMatrix.smx
echo :: direct sky matrix
c:\radiance\bin\gendaymtx -d -O0 -r 0.0 -m 1 -v sky/skymtx_vis_r1_1_061800_55.63_12.67_0.0_SkyMatrix.wea > sky/skymtx_vis_r1_1_061800_55.63_12.67_0.0_SkyMatrix.smx
echo :: Done with 0 of 2 ^|----------^| (0.00%%)
echo ::
echo :: start of the calculation for scene, default. State 1 of 1
echo ::
echo :: :: 1. calculating daylight matrices
echo ::
echo :: :: [1/3] scene daylight matrix
echo :: :: rfluxmtx - [sky] [points] [wgroup] [blacked wgroups] [scene] ^> [dc.mtx]
echo ::
c:\radiance\bin\rfluxmtx -y 108 -aa 0.25 -ab 3 -ad 5000 -ar 16 -as 128 -dc 0.25 -dj 0.0 -dp 64 -ds 0.5 -dr 0 -dt 0.5 -I -lr 4 -lw 2e-06 -c 1 -ss 0.0 -st 0.85 - sky\rfluxSky.rad scene\glazing\DaylightAnalysis..glz.mat scene\glazing\DaylightAnalysis..glz.rad scene\opaque\DaylightAnalysis..opq.mat scene\opaque\DaylightAnalysis..opq.rad scene\extra\context.rad scene\wgroup\black.mat scene\wgroup\Window_88..blk.rad < DaylightAnalysis.pts > result\matrix\normal_DaylightAnalysis..scene..default.dc 
echo :: :: [2/3] black scene daylight matrix
echo :: :: rfluxmtx - [sky] [points] [wgroup] [blacked wgroups] [blacked scene] ^> [black dc.mtx]
echo ::
c:\radiance\bin\rfluxmtx -y 108 -aa 0.25 -ab 1 -ad 5000 -ar 16 -as 128 -dc 0.25 -dj 0.0 -dp 64 -ds 0.5 -dr 0 -dt 0.5 -I -lr 4 -lw 2e-06 -c 1 -ss 0.0 -st 0.85 - sky\rfluxSky.rad scene\glazing\DaylightAnalysis..glz.mat scene\glazing\DaylightAnalysis..glz.rad scene\opaque\DaylightAnalysis..blk.mat scene\opaque\DaylightAnalysis..opq.rad scene\extra\black.mat scene\extra\context_blacked.rad scene\wgroup\black.mat scene\wgroup\Window_88..blk.rad < DaylightAnalysis.pts > result\matrix\black_DaylightAnalysis..scene..default.dc 
echo :: :: [3/3] black scene analemma daylight matrix
echo :: :: rcontrib - [sun_matrix] [points] [wgroup] [blacked wgroups] [blacked scene] ^> [analemma dc.mtx]
echo ::
c:\radiance\bin\oconv -f scene\glazing\DaylightAnalysis..glz.mat scene\glazing\DaylightAnalysis..glz.rad scene\opaque\DaylightAnalysis..blk.mat scene\opaque\DaylightAnalysis..opq.rad scene\extra\black.mat scene\extra\context_blacked.rad scene\wgroup\black.mat scene\wgroup\Window_88..blk.rad sky\analemma_reversed.rad > analemma.oct
c:\radiance\bin\rcontrib -aa 0.0 -ab 0 -ad 512 -ar 16 -as 128 -dc 1.0 -dj 0.0 -dp 64 -ds 0.5 -dr 0 -dt 0.0 -I -lr 4 -lw 0.05 -M .\sky\analemma.mod -ss 0.0 -st 0.85 analemma.oct < DaylightAnalysis.pts > result\matrix\sun_DaylightAnalysis..scene..default.dc
echo :: :: 2. matrix multiplication
echo ::
echo :: :: [1/3] calculating daylight mtx * total sky
echo :: :: dctimestep [dc.mtx] [total sky] ^> [total results.rgb]
c:\radiance\bin\dctimestep result\matrix\normal_DaylightAnalysis..scene..default.dc sky\skymtx_vis_r1_0_061800_55.63_12.67_0.0_SkyMatrix.smx > tmp\total..scene..default.rgb
echo :: :: rmtxop -c 47.4 119.9 11.6 [results.rgb] ^> [total results.ill]
echo ::
c:\radiance\bin\rmtxop -c 47.4 119.9 11.6 -fa tmp\total..scene..default.rgb > result\total..scene..default.ill
echo :: :: [2/3] calculating black daylight mtx * direct only sky
echo :: :: dctimestep [black dc.mtx] [direct only sky] ^> [direct results.rgb]
c:\radiance\bin\dctimestep result\matrix\black_DaylightAnalysis..scene..default.dc sky\skymtx_vis_r1_1_061800_55.63_12.67_0.0_SkyMatrix.smx > tmp\direct..scene..default.rgb
echo :: :: rmtxop -c 47.4 119.9 11.6 [direct results.rgb] ^> [direct results.ill]
echo ::
c:\radiance\bin\rmtxop -c 47.4 119.9 11.6 -fa tmp\direct..scene..default.rgb > result\direct..scene..default.ill
echo :: :: [3/3] calculating black daylight mtx * analemma
echo :: :: dctimestep [black dc.mtx] [analemma only sky] ^> [sun results.rgb]
c:\radiance\bin\dctimestep result\matrix\sun_DaylightAnalysis..scene..default.dc sky\sunmtx.smx > tmp\sun..scene..default.rgb
echo :: :: rmtxop -c 47.4 119.9 11.6 [sun results.rgb] ^> [sun results.ill]
echo ::
c:\radiance\bin\rmtxop -c 47.4 119.9 11.6 -fa tmp\sun..scene..default.rgb > result\sun..scene..default.ill
echo :: :: 3. calculating final results
echo :: :: rmtxop [total results.ill] - [direct results.ill] + [sun results.ill] ^> [final results.ill]
echo ::
c:\radiance\bin\rmtxop result\total..scene..default.ill + -s -1.0 result\direct..scene..default.ill + result\sun..scene..default.ill > result\scene..default.ill
echo :: end of calculation for scene, default
echo ::
echo ::
echo :: start of the 3-phase calculation for the window group Window_88
echo :: :: [1/3] calculating view matrix
echo :: :: rfluxmtx - [wgroup] [scene] [points] [blacked wgroups] ^> [*.vmx]
echo ::
c:\radiance\bin\rfluxmtx -y 108 -aa 0.1 -ab 7 -ad 20000 -ar 128 -as 4096 -dc 0.75 -dj 1.0 -dp 512 -ds 0.05 -dr 3 -dt 0.15 -I -lr 8 -lw 5e-07 -ss 1.0 -st 0.15 - scene\wgroup\Window_88..glw.rad scene\opaque\DaylightAnalysis..opq.mat scene\opaque\DaylightAnalysis..opq.rad scene\wgroup\black.mat scene\glazing\DaylightAnalysis..blk.mat scene\glazing\DaylightAnalysis..glz.rad < DaylightAnalysis.pts > result\matrix\Window_88.vmx 
echo :: :: [2/3] calculating daylight matrix
echo :: :: rfluxmtx - [sky] [points] [wgroup] [blacked wgroups] [scene] ^> [*.dmx]
echo ::
c:\radiance\bin\rfluxmtx -aa 0.1 -ab 6 -ad 10000 -ar 128 -as 4096 -dc 0.75 -dj 1.0 -dp 512 -ds 0.05 -dr 3 -dt 0.15  -lr 8 -lw 1e-06 -c 1000 -ss 1.0 -st 0.15 scene\wgroup\Window_88..glw.rad sky\rfluxSky.rad scene\opaque\DaylightAnalysis..opq.mat scene\opaque\DaylightAnalysis..opq.rad scene\extra\context.rad scene\wgroup\black.mat scene\glazing\DaylightAnalysis..blk.mat scene\glazing\DaylightAnalysis..glz.rad > result\matrix\Window_88_1.dmx 
echo :: :: State default [1 out of 1]
echo :: :: [3/3] v_matrix * d_matrix * t_matrix
echo :: :: dctimestep [vmx] [tmtx] [dmtx] ^ > [results.rgb]
c:\radiance\bin\dctimestep result/matrix/Window_88.vmx scene\bsdf\00001.xml result\matrix\Window_88_1.dmx sky\skymtx_vis_r1_0_061800_55.63_12.67_0.0_SkyMatrix.smx > tmp\Window_88..default.tmp
echo :: :: rmtxop -c 47.4 119.9 11.6 [results.rgb] ^> [results.ill]
echo ::
echo ::
c:\radiance\bin\rmtxop -c 47.4 119.9 11.6 -fa tmp\Window_88..default.tmp > result\Window_88..default.ill