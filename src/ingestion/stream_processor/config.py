SPARK_SERVER = "spark://127.0.0.1:7077"

TICKERS = ['AAA', 'AAM', 'AAT', 'ABR', 'ABS', 'ABT', 'ACB', 'ACC', 'ACL', 'ADG', 
'ADS', 'AGG', 'AGM', 'AGR', 'AMD', 'ANV', 'APC', 'APG', 'APH', 'ASG', 
'ASM', 'ASP', 'AST', 'BAF', 'BBC', 'BCE', 'BCG', 'BCM', 'BFC', 'BHN', 
'BIC', 'BID', 'BKG', 'BMC', 'BMI', 'BMP', 'BRC', 'BSI', 'BTP', 'BTT', 
'BVH', 'BWE', 'C32', 'C47', 'CAV', 'CCI', 'CCL', 'CDC', 'CHP', 'CIG', 
'CII', 'CKG', 'CLC', 'CLL', 'CLW', 'CMG', 'CMV', 'CMX', 'CNG', 'COM', 
'CRC', 'CRE', 'CSM', 'CSV', 'CTD', 'CTF', 'CTG', 'CTI', 'CTR', 'CTS', 
'CVT', 'D2D', 'DAG', 'DAH', 'DAT', 'DBC', 'DBD', 'DBT', 'DC4', 'DCL', 
'DCM', 'DGC', 'DGW', 'DHA', 'DHC', 'DHG', 'DHM', 'DIG', 'DLG', 'DMC', 
'DPG', 'DPM', 'DPR', 'DQC', 'DRC', 'DRH', 'DRL', 'DSN', 'DTA', 'DTL', 
'DTT', 'DVP', 'DXG', 'DXS', 'DXV', 'EIB', 'ELC', 'EMC', 'EVE', 'EVF', 
'EVG', 'FCM', 'FCN', 'FDC', 'FIR', 'FIT', 'FLC', 'FMC', 'FPT', 'FRT', 
'FTS', 'GAB', 'GAS', 'GDT', 'GEG', 'GEX', 'GIL', 'GMC', 'GMD', 'GMH', 
'GSP', 'GTA', 'GVR', 'HAG', 'HAH', 'HAI', 'HAP', 'HAR', 'HAS', 'HAX', 
'HBC', 'HCD', 'HCM', 'HDB', 'HDC', 'HDG', 'HHP', 'HHS', 'HHV', 'HID', 
'HII', 'HMC', 'HNG', 'HOT', 'HPG', 'HPX', 'HQC', 'HRC', 'HSG', 'HSL', 
'HT1', 'HTI', 'HTL', 'HTN', 'HTV', 'HU1', 'HU3', 'HUB', 'HVH', 'HVN', 
'HVX', 'IBC', 'ICT', 'IDI', 'IJC', 'ILB', 'IMP', 'ITA', 'ITC', 'ITD', 
'JVC', 'KBC', 'KDC', 'KDH', 'KHG', 'KHP', 'KMR', 'KOS', 'KPF', 'KSB', 
'L10', 'LAF', 'LBM', 'LCG', 'LCM', 'LDG', 'LEC', 'LGC', 'LGL', 'LHG', 
'LIX', 'LM8', 'LPB', 'LSS', 'MBB', 'MCG', 'MCP', 'MDG', 'MHC', 'MIG', 
'MSB', 'MSH', 'MSN', 'MWG', 'NAF', 'NAV', 'NBB', 'NCT', 'NHA', 'NHH', 
'NHT', 'NKG', 'NLG', 'NNC', 'NSC', 'NT2', 'NTL', 'NVL', 'NVT', 'OCB', 
'OGC', 'OPC', 'ORS', 'PAC', 'PAN', 'PC1', 'PDN', 'PDR', 'PET', 'PGC', 
'PGD', 'PGI', 'PGV', 'PHC', 'PHR', 'PIT', 'PJT', 'PLP', 'PLX', 'PMG', 
'PNC', 'PNJ', 'POM', 'POW', 'PPC', 'PSH', 'PTB', 'PTC', 'PTL', 'PVD', 
'PVT', 'QBS', 'QCG', 'RAL', 'RDP', 'REE', 'ROS', 'S4A', 'SAB', 'SAM', 
'SAV', 'SBA', 'SBT', 'SBV', 'SC5', 'SCD', 'SCR', 'SCS', 'SFC', 'SFG', 
'SFI', 'SGN', 'SGR', 'SGT', 'SHA', 'SHB', 'SHI', 'SHP', 'SII', 'SJD', 
'SJF', 'SJS', 'SKG', 'SMA', 'SMB', 'SMC', 'SPM', 'SRC', 'SRF', 'SSB', 
'SSC', 'SSI', 'ST8', 'STB', 'STG', 'STK', 'SVC', 'SVD', 'SVI', 'SVT', 
'SZC', 'SZL', 'TBC', 'TCB', 'TCD', 'TCH', 'TCL', 'TCM', 'TCO', 'TCR', 
'TCT', 'TDC', 'TDG', 'TDH', 'TDM', 'TDP', 'TDW', 'TEG', 'TGG', 'THG', 
'THI', 'TIP', 'TIX', 'TLD', 'TLG', 'TLH', 'TMP', 'TMS', 'TMT', 'TN1', 
'TNA', 'TNC', 'TNH', 'TNI', 'TNT', 'TPB', 'TPC', 'TRA', 'TRC', 'TSC', 
'TTA', 'TTB', 'TTE', 'TTF', 'TV2', 'TVB', 'TVS', 'TVT', 'TYA', 'UDC', 
'UIC', 'VAF', 'VCA', 'VCB', 'VCF', 'VCG', 'VCI', 'VDP', 'VDS', 'VFG', 
'VGC', 'VHC', 'VHM', 'VIB', 'VIC', 'VID', 'VIP', 'VIX', 'VJC', 'VMD', 
'VND', 'VNE', 'VNG', 'VNL', 'VNM', 'VNS', 'VOS', 'VPB', 'VPD', 'VPG', 
'VPH', 'VPI', 'VPS', 'VRC', 'VRE', 'VSC', 'VSH', 'VSI', 'VTB', 'VTO', 
'YBM', 'YEG', 'AAV', 'ADC', 'ALT', 'AMC', 'AME', 'AMV', 'API', 'APS', 'ARM', 'ART', 
'ATS', 'BAB', 'BAX', 'BBS', 'BCC', 'BCF', 'BDB', 'BED', 'BII', 'BKC', 
'BLF', 'BNA', 'BPC', 'BSC', 'BST', 'BTS', 'BTW', 'BVS', 'BXH', 'C69', 
'CAG', 'CAN', 'CAP', 'CCR', 'CDN', 'CEO', 'CET', 'CIA', 'CJC', 'CKV', 
'CLH', 'CLM', 'CMC', 'CMS', 'CPC', 'CSC', 'CTB', 'CTC', 'CTP', 'CTT', 
'CTX', 'CVN', 'CX8', 'D11', 'DAD', 'DAE', 'DC2', 'DDG', 'DHP', 'DHT', 
'DIH', 'DL1', 'DNC', 'DNM', 'DNP', 'DP3', 'DPC', 'DS3', 'DST', 'DTC', 
'DTD', 'DTK', 'DVG', 'DXP', 'DZM', 'EBS', 'ECI', 'EID', 'EVS', 
'FID', 'GDW', 'GIC', 'GKM', 'GLT', 'GMA', 'GMX', 'HAD', 'HAT', 'HBS', 
'HCC', 'HCT', 'HDA', 'HEV', 'HGM', 'HHC', 'HHG', 'HJS', 'HKT', 'HLC', 
'HLD', 'HMH', 'HMR', 'HOM', 'HTC', 'HTP', 'HUT', 'HVT', 'ICG', 'IDC', 
'IDJ', 'IDV', 'INC', 'INN', 'IPA', 'ITQ', 'IVS', 'KDM', 'KHS', 'KKC', 
'KLF', 'KMT', 'KSD', 'KSF', 'KSQ', 'KST', 'KTS', 'KTT', 'KVC', 'L14', 
'L18', 'L35', 'L40', 'L43', 'L61', 'L62', 'LAS', 'LBE', 'LCD', 'LCS', 
'LDP', 'LHC', 'LIG', 'LM7', 'LUT', 'MAC', 'MAS', 'MBG', 'MBS', 'MCC', 
'MCF', 'MCO', 'MDC', 'MED', 'MEL', 'MHL', 'MIM', 'MKV', 'MST', 'MVB', 
'NAG', 'NAP', 'NBC', 'NBP', 'NBW', 'NDN', 'NDX', 'NET', 'NFC', 'NHC',
'NRC', 'NSH', 'NST', 'NTH', 'NTP', 'NVB', 'OCH', 'ONE', 'PBP', 'PCE', 
'PCG', 'PCT', 'PDB', 'PEN', 'PGN', 'PGS', 'PGT', 'PHN', 'PHP', 
'PIA', 'PIC', 'PJC', 'PLC', 'PMB', 'PMC', 'PMP', 'PMS', 'POT', 'PPE', 
'PPP', 'PPS', 'PPY', 'PRC', 'PRE', 'PSC', 'PSD', 'PSE', 'PSI', 'PSW', 
'PTD', 'PTI', 'PTS', 'PV2', 'PVB', 'PVC', 'PVG', 'PVI', 'PVL', 'PVS', 
'QHD', 'QST', 'QTC', 'RCL', 'S55', 'S99', 'SAF', 'SCG', 'SCI', 'SD4', 
'SD5', 'SD6', 'SD9', 'SDA', 'SDC', 'SDG', 'SDN', 'SDT', 'SDU', 'SEB', 
'SED', 'SFN', 'SGC', 'SGD', 'SGH', 'SHE', 'SHN', 'SHS', 'SIC', 'SJ1', 
'SJE', 'SLS', 'SMN', 'SMT', 'SPC', 'SPI', 'SRA', 'SSM', 'STC', 'STP', 
'SVN', 'SZB', 'TA9', 'TAR', 'TBX', 'TC6', 'TDN', 'TDT', 'TET', 'TFC', 
'THB', 'THD', 'THS', 'THT', 'TIG', 'TJC', 'TKC', 'TKU', 'TMB', 'TMC', 
'TMX', 'TNG', 'TOT', 'TPH', 'TPP', 'TSB', 'TTC', 'TTH', 'TTL', 'TTT', 
'TTZ', 'TV3', 'TV4', 'TVC', 'TVD', 'TXM', 'UNI', 'V12', 'V21', 'VBC', 
'VC1', 'VC2', 'VC3', 'VC6', 'VC7', 'VC9', 'VCC', 'VCM', 'VCS', 'VDL', 
'VE1', 'VE2', 'VE3', 'VE4', 'VE8', 'VGP', 'VGS', 'VHE', 'VHL', 'VIF', 
'VIG', 'VIT', 'VKC', 'VLA', 'VMC', 'VMS', 'VNC', 'VNF', 'VNR', 'VNT', 
'VSA', 'VSM', 'VTC', 'VTH', 'VTJ', 'VTL', 'VTV', 'VTZ', 'WCS', 'WSS', 
'X20']



#db config
host = '127.0.0.1'
database = 'StockAlertingSystem'
username = ''
password = ''
port = 

influx_token = ""
influx_org = "HUST"
influx_bucket = "market_data"
influx_server = ""

# ssi config
auth_type = 'Bearer'
consumerID = ''
consumerSecret = ''
access_jwt = ''
url = 'https://fc-data.ssi.com.vn/'
stream_url = 'https://fc-data.ssi.com.vn/'
