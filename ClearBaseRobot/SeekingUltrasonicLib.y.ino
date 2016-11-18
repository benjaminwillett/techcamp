
long Seek(int dest){
  static int angle=0;
  long dist;
  while (angle<dest){
    moveStepper(1);
    angle+=1;
  }
  while (angle>dest){
    moveStepper(-1);
    angle-=1;
  }
  dist = echo_dist();
  Serial.print(dist);
  Serial.println(" cm");
  return dist;
}

