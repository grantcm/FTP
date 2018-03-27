with open('1_0_input','w') as f:
  f.write('CONNECT classroo.cs.unc.edu 9631\n')
  f.write('GET doesnotexist\n')
  f.write('QUIT\n')
  f.write('')

with open('1_0_output_client','w') as f:
  f.write('CONNECT classroo.cs.unc.edu 9631\n')
  f.write('CONNECT accepted for FTP server at host classroo.cs.unc.edu and port 9631\n')
  f.write('CONNECT failed\n')
  f.write('GET doesnotexist\n')
  f.write('ERROR -- expecting CONNECT\n')
  f.write('QUIT\n')
  f.write('ERROR -- expecting CONNECT\n')
  f.write('')

with open('1_0_output_server','w') as f:
  f.write('')

