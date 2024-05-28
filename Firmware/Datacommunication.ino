
  
  void writeSensorStream() 
  {
  byte header[] = {0xFF, 0xFF, 0x00};
  byte chksum = 0xFE;
  byte _temp;
  byte _force;


//Out data buffer
  outPayload.newPacket();
  outPayload.add(gyrox1);
  outPayload.add(gyroy1);
  outPayload.add(gyroz1);
  outPayload.add(accelx1);
  outPayload.add(accely1);
  outPayload.add(accelz1);
  outPayload.add(counter);
  outPayload.add(delt);
  outPayload.add(sync);
 
//  send packet
 header[2] = outPayload.sz()*2+1;
 chksum += header[2]; 
 
// Send header
  Serial1.write(header[0]);
  Serial1.write(header[1]);
 Serial1.write(header[2]);
  
  // Send payload
  for (int i = 0; i < outPayload.sz() * 2; i++) {
    _temp = outPayload.getByte(i);
    Serial1.write(_temp);
    chksum += _temp;
  }
    
Serial1.write(chksum);
}
