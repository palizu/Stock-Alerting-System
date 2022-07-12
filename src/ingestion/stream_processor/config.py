TICKERS = ['AAA', 'AAM', 'AAT', 'ABR', 'ABS', 'ABT', 'ACB', 'ACC', 'ACL', 'ADG', 'ADS', 'AGG', 'AGM', 'AGR', 'AMD', 
                'ANV', 'APC', 'APG', 'APH', 'ASG', 'ASM', 'ASP', 'AST', 'BAF', 'BBC', 'BCE', 'BCG', 'BCM', 'BFC', 'BHN', 
                'BIC', 'BID', 'BKG', 'BMC', 'BMI', 'BMP', 'BRC', 'BSI', 'BTP', 'BTT', 'BVH', 'BWE', 'C32', 'C47', 'CACB2102', 
                'CACB2201', 'CACB2202', 'CACB2203', 'CAV', 'CCI', 'CCL', 'CDC', 'CEE', 'CFPT2108', 'CFPT2201', 'CFPT2202', 'CFPT2203', 
                'CHDB2201', 'CHDB2202', 'CHDB2203', 'CHDB2204', 'CHDB2205', 'CHP', 'CHPG2116', 'CHPG2117', 'CHPG2201', 'CHPG2202', 
                'CHPG2203', 'CHPG2204', 'CHPG2206', 'CHPG2207', 'CHPG2208', 'CHPG2209', 'CHPG2210', 'CHPG2211', 'CIG', 'CII', 
                'CKDH2201', 'CKDH2202', 'CKDH2203', 'CKDH2204', 'CKDH2205', 'CKDH2206', 'CKG', 'CLC', 'CLL', 'CLW', 'CMBB2201', 
                'CMBB2203', 'CMG', 'CMSN2201', 'CMSN2202', 'CMSN2203', 'CMV', 'CMWG2201', 'CMWG2202', 'CMWG2203', 'CMWG2204', 'CMX', 
                'CNG', 'CNVL2201', 'CNVL2202', 'CNVL2203', 'CNVL2204', 'COM', 'CPDR2201', 'CPDR2202', 'CPDR2203', 'CPNJ2201', 'CPOW2201', 
                'CPOW2202', 'CPOW2203', 'CRC', 'CRE', 'CSM', 'CSTB2201', 'CSTB2202', 'CSTB2203', 'CSTB2205', 'CSTB2206', 'CSTB2207', 'CSTB2208', 
                'CSTB2209', 'CSV', 'CTCB2112', 'CTCB2201', 'CTCB2202', 'CTCB2203', 'CTCB2204', 'CTCB2205', 'CTD', 'CTF', 'CTG', 'CTI', 'CTPB2201', 
                'CTPB2202', 'CTR', 'CTS', 'CVHM2113', 'CVHM2115', 'CVHM2201', 'CVHM2202', 'CVHM2203', 'CVHM2204', 'CVHM2205', 'CVHM2206', 'CVHM2207', 
                'CVIC2201', 'CVIC2202', 'CVIC2203', 'CVIC2204', 'CVIC2205', 'CVIC2206', 'CVJC2201', 'CVJC2202', 'CVNM2201', 'CVNM2202', 'CVNM2203', 
                'CVNM2204', 'CVNM2205', 'CVNM2206', 'CVPB2201', 'CVPB2202', 'CVPB2203', 'CVPB2204', 'CVPB2205', 'CVRE2201', 'CVRE2202', 'CVRE2203', 
                'CVRE2204', 'CVRE2205', 'CVRE2206', 'CVRE2207', 'CVT', 'D2D', 'DAG', 'DAH', 'DAT', 'DBC', 'DBD', 'DBT', 'DC4', 'DCL', 'DCM', 'DGC', 
                'DGW', 'DHA', 'DHC', 'DHG', 'DHM', 'DIG', 'DLG', 'DMC', 'DPG', 'DPM', 'DPR', 'DQC', 'DRC', 'DRH', 'DRL', 'DSN', 'DTA', 'DTL', 'DTT', 
                'DVP', 'DXG', 'DXS', 'DXV', 'E1VFVN30', 'EIB', 'ELC', 'EMC', 'EVE', 'EVF', 'EVG', 'FCM', 'FCN', 'FDC', 'FIR', 'FIT', 'FLC', 'FMC', 
                'FPT', 'FRT', 'FTS', 'FUCTVGF3', 'FUCVREIT', 'FUEIP100', 'FUEKIV30', 'FUEMAV30', 'FUESSV30', 'FUESSV50', 'FUESSVFL', 'FUEVFVND', 
                'FUEVN100', 'GAB', 'GAS', 'GDT', 'GEG', 'GEX', 'GIL', 'GMC', 'GMD', 'GMH', 'GSP', 'GTA', 'GVR', 'HAG', 'HAH', 'HAI', 'HAP', 'HAR', 
                'HAS', 'HAX', 'HBC', 'HCD', 'HCM', 'HCMA0307', 'HCM_0307', 'HCM_0607', 'HCM_0807', 'HCM_1007', 'HDB', 'HDC', 'HDG', 'HHP', 'HHS', 
                'HHV', 'HID', 'HII', 'HMC', 'HNG', 'HOT', 'HPG', 'HPX', 'HQC', 'HRC', 'HSG', 'HSL', 'HT1', 'HTI', 'HTL', 'HTN', 'HTV', 'HU1', 
                'HU3', 'HUB', 'HVH', 'HVN', 'HVX', 'IBC', 'ICT', 'IDI', 'IJC', 'ILB', 'IMP', 'ITA', 'ITC', 'ITD', 'JVC', 'KBC', 'KDC', 'KDH', 
                'KHG', 'KHP', 'KMR', 'KOS', 'KPF', 'KSB', 'L10', 'LAF', 'LBM', 'LCG', 'LCM', 'LDG', 'LEC', 'LGC', 'LGL', 'LHG', 'LIX', 'LM8', 
                'LPB', 'LSS', 'MBB', 'MCG', 'MCP', 'MDG', 'MHC', 'MIG', 'MSB', 'MSH', 'MSN', 'MSN11906', 'MSN12001', 'MSN12002', 'MSN12003', 
                'MSN12005', 'MWG', 'NAF', 'NAV', 'NBB', 'NCT', 'NHA', 'NHH', 'NHT', 'NKG', 'NLG', 'NNC', 'NPM11805', 'NPM11907', 'NPM11910', 
                'NPM11911', 'NSC', 'NT2', 'NTL', 'NVL', 'NVT', 'OCB', 'OGC', 'OPC', 'ORS', 'PAC', 'PAN', 'PC1', 'PDN', 'PDR', 'PET', 'PGC', 
                'PGD', 'PGI', 'PGV', 'PHC', 'PHR', 'PIT', 'PJT', 'PLP', 'PLX', 'PMG', 'PNC', 'PNJ', 'POM', 'POW', 'PPC', 'PSH', 'PTB', 'PTC', 
                'PTL', 'PVD', 'PVT', 'PXS', 'QBS', 'QCG', 'RAL', 'RDP', 'REE', 'ROS', 'S4A', 'SAB', 'SAM', 'SAV', 'SBA', 'SBT', 'SBV', 'SC5', 
                'SCD', 'SCR', 'SCS', 'SFC', 'SFG', 'SFI', 'SGN', 'SGR', 'SGT', 'SHA', 'SHB', 'SHI', 'SHP', 'SII', 'SJD', 'SJF', 'SJS', 'SKG', 
                'SMA', 'SMB', 'SMC', 'SPM', 'SRC', 'SRF', 'SSB', 'SSC', 'SSI', 'ST8', 'STB', 'STG', 'STK', 'SVC', 'SVD', 'SVI', 'SVT', 'SZC', 
                'SZL', 'TBC', 'TCB', 'TCD', 'TCH', 'TCL', 'TCM', 'TCO', 'TCR', 'TCT', 'TDC', 'TDG', 'TDH', 'TDM', 'TDP', 'TDW', 'TEG', 'TGG', 
                'THG', 'THI', 'TIP', 'TIX', 'TLD', 'TLG', 'TLH', 'TMP', 'TMS', 'TMT', 'TN1', 'TNA', 'TNC', 'TNH', 'TNI', 'TNT', 'TPB', 'TPC', 
                'TRA', 'TRC', 'TSC', 'TTA', 'TTB', 'TTE', 'TTF', 'TV2', 'TVB', 'TVS', 'TVT', 'TYA', 'UDC', 'UIC', 'VAF', 'VCA', 'VCB', 'VCF', 
                'VCG', 'VCI', 'VDP', 'VDS', 'VFG', 'VGC', 'VHC', 'VHM', 'VIB', 'VIC', 'VID', 'VIP', 'VIX', 'VJC', 'VJC11912', 'VMD', 'VND', 
                'VNE', 'VNG', 'VNL', 'VNM', 'VNS', 'VOS', 'VPB', 'VPD', 'VPG', 'VPH', 'VPI', 'VPS', 'VRC', 'VRE', 'VRE12007', 'VSC', 'VSH', 
                'VSI', 'VTB', 'VTO', 'YBM', 'YEG', 'AAV', 'ACM', 'ADC', 'ALT', 'AMC', 'AME', 'AMV', 'API', 'APP', 'APS', 'ARM', 'ART', 'ATS', 
                'BAB', 'BAX', 'BBS', 'BCC', 'BCF', 'BDB', 'BED', 'BII', 'BKC', 'BLF', 'BNA', 'BPC', 'BSC', 'BST', 'BTS', 'BTW', 'BVS', 'BXH', 
                'C69', 'C92', 'CAG', 'CAN', 'CAP', 'CCR', 'CDN', 'CEO', 'CET', 'CIA', 'CII120018', 'CJC', 'CKV', 'CLH', 'CLM', 'CMC', 'CMS', 
                'CPC', 'CSC', 'CTB', 'CTC', 'CTP', 'CTT', 'CTX', 'CVN', 'CX8', 'D11', 'DAD', 'DAE', 'DC2', 'DDG', 'DHP', 'DHT', 'DIH', 'DL1', 
                'DNC', 'DNM', 'DNP', 'DP3', 'DPC', 'DS3', 'DST', 'DTC', 'DTD', 'DTK', 'DVG', 'DXP', 'DZM', 'EBS', 'ECI', 'EID', 'EVS', 'FID', 
                'GDW', 'GIC', 'GKM', 'GLT', 'GMA', 'GMX', 'HAD', 'HAT', 'HBS', 'HCC', 'HCT', 'HDA', 'HDG121001', 'HEV', 'HGM', 'HHC', 'HHG', 
                'HJS', 'HKT', 'HLC', 'HLD', 'HMH', 'HMR', 'HOM', 'HPM', 'HTC', 'HTP', 'HUT', 'HVT', 'ICG', 'IDC', 'IDJ', 'IDV', 'INC', 'INN', 
                'IPA', 'ITQ', 'IVS', 'KDM', 'KHS', 'KKC', 'KLF', 'KMT', 'KSD', 'KSF', 'KSQ', 'KST', 'KTS', 'KTT', 'KVC', 'L14', 'L18', 'L35', 
                'L40', 'L43', 'L61', 'L62', 'LAS', 'LBE', 'LCD', 'LCS', 'LDP', 'LHC', 'LIG', 'LM7', 'LUT', 'MAC', 'MAS', 'MBG', 'MBS', 'MCC', 
                'MCF', 'MCO', 'MDC', 'MED', 'MEL', 'MHL', 'MIM', 'MKV', 'MSR11808', 'MST', 'MVB', 'NAG', 'NAP', 'NBC', 'NBP', 'NBW', 'NDN', 
                'NDX', 'NET', 'NFC', 'NHC', 'NRC', 'NSH', 'NST', 'NTH', 'NTP', 'NVB', 'OCH', 'ONE', 'PBP', 'PCE', 'PCG', 'PCT', 'PDB', 'PDC', 
                'PEN', 'PGN', 'PGS', 'PGT', 'PHN', 'PHP', 'PIA', 'PIC', 'PJC', 'PLC', 'PMB', 'PMC', 'PMP', 'PMS', 'POT', 'PPE', 'PPP', 'PPS', 
                'PPY', 'PRC', 'PRE', 'PSC', 'PSD', 'PSE', 'PSI', 'PSW', 'PTD', 'PTI', 'PTS', 'PV2', 'PVB', 'PVC', 'PVG', 'PVI', 'PVL', 'PVS', 
                'QHD', 'QST', 'QTC', 'RCL', 'S55', 'S99', 'SAF', 'SCG', 'SCI', 'SD2', 'SD4', 'SD5', 'SD6', 'SD9', 'SDA', 'SDC', 'SDG', 'SDN', 
                'SDT', 'SDU', 'SEB', 'SED', 'SFN', 'SGC', 'SGD', 'SGH', 'SHE', 'SHN', 'SHS', 'SHT119008', 'SHT119009', 'SIC', 'SJ1', 'SJE', 
                'SLS', 'SMN', 'SMT', 'SPC', 'SPI', 'SRA', 'SSM', 'STC', 'STP', 'SVN', 'SZB', 'TA9', 'TAR', 'TBX', 'TC6', 'TDN', 'TDT', 'TET', 
                'TFC', 'THB', 'THD', 'THS', 'THT', 'TIG', 'TJC', 'TKC', 'TKU', 'TMB', 'TMC', 'TMX', 'TNG', 'TNG119007', 'TOT', 'TPH', 'TPP', 
                'TSB', 'TST', 'TTC', 'TTH', 'TTL', 'TTT', 'TTZ', 'TV3', 'TV4', 'TVC', 'TVD', 'TXM', 'UNI', 'V12', 'V21', 'VBC', 'VC1', 'VC2', 
                'VC3', 'VC6', 'VC7', 'VC9', 'VCC', 'VCM', 'VCS', 'VDL', 'VE1', 'VE2', 'VE3', 'VE4', 'VE8', 'VGP', 'VGS', 'VHE', 'VHL', 'VIE', 
                'VIF', 'VIG', 'VIT', 'VKC', 'VLA', 'VMC', 'VMS', 'VNC', 'VNF', 'VNR', 'VNT', 'VSA', 'VSM', 'VTC', 'VTH', 'VTJ', 'VTL', 'VTV', 
                'VTZ', 'VXB', 'WCS', 'WSS', 'X20']  



#db config
host = '127.0.0.1'
database = 'StockAlertingSystem'
username = 'root'
password = ''
port = 3306

# ssi config
auth_type = 'Bearer'
consumerID = ''
consumerSecret = ''
access_jwt = ''
url = 'https://fc-data.ssi.com.vn/'
stream_url = 'https://fc-data.ssi.com.vn/'