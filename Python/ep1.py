def main():   #vou ter q converter o possível 02 pra 2
  END=0 #valor final
  mes31 = [0, 1, 0, 3, 0, 5, 0, 7, 8, 0, 10, 0, 12,2,3, 4, 6, 9, 11]
  mes30 = [0, 0, 0, 0, 4, 0, 6, 0, 0, 9, 10, 11, 0, 1, 5, 7,  8, 10, 12,2]
  total_mes=0  #total de horas mês
  bissexto=0  #variavel que vai mudar de acordo com o ano bissexto no range de fevereiro
  total_anos = 0  #quantidade de anos no intervalo
  total_inicial=0  #parcela de horas relativa ao primeiro ano
  total_final=0  #parcela de horas relativa ao ultimo ano
  inicial_d=int(input("Digite o dia inicial: "))
  inicial_m=int(input("Digite o mês inicial: "))
  inicial_a=int(input("Digite o ano inicial: "))
  inicial_h=int(input("Digite a hora inicial: "))
  final_d=int(input("Digite o dia final: "))
  final_m=int(input("Digite o mês final: "))
  final_a=int(input("Digite o ano final: "))
  final_h=int(input("Digite a hora final: "))
  month30= mes30.index(inicial_m) #lista de meses 30
  month31= mes31.index(inicial_m) # lista de meses 31
  meses=[1,2,3,4,5,6,7,8,9,10,11,12]
  days=0
  years=0
  leap=0

  for i in range(inicial_a+1, final_a):
    years += 1
    if i % 4 == 0:
      if i % 100 > 0:
        leap += 1
        bissexto = 1
      else:
        if i % 400 == 0:
          leap += 1


  if final_a % 4 == 0:
    if final_a % 100 > 0:
      leap += 1
      bissexto = 1
    else:
      if final_a % 400 == 0:
        leap += 1
        bissexto = 1

  if final_a-inicial_a>0:
    total_anos = (years * 8760) + (leap * 24)

  if 0<mes31.index(inicial_m)<=12:
    for i in range(inicial_d, 32):
      days += 1


  elif 0<mes30.index(inicial_m)<=12:
    for i in range(inicial_d,31):
      days+=1



  if inicial_m== 2:
    if bissexto==0:
      for i in range(inicial_d,29):
        days+=1



    elif bissexto==1:
      for i in range(inicial_d,30):
        days+=1



  if final_a-inicial_a>1:
    if inicial_m==1:
      days+=334
    elif inicial_m==2:
      days+=306
    elif inicial_m==3:
      days+=275
    elif inicial_m==4:
      days+=245
    elif inicial_m==5:
      days+=214
    elif inicial_m==6:
      days+=  184
    elif inicial_m==7:
      days+=153
    elif inicial_m==8:
      days+=122
    elif inicial_m==9:
      days+=92
    elif inicial_m==10:
      days+=61
    elif inicial_m==11:
      days+=31
  total_inicial = (days * 24) - inicial_h
  days=0



  if final_d-inicial_d>1:
   if 0<mes31.index(final_m)<=12:
     for i in range(1,final_d+1):
       days+= 1
   elif 0<mes30.index(final_m)<=12:
     for i in range(1,final_d+1):
       days+=1

   elif final_m== 2:
     if bissexto == 0:
       for i in range(1, final_d+1):
         days += 1

     elif bissexto == 1:
       for i in range(1, final_d+1):
         days += 1

  if final_a-inicial_a>1:
    if final_m==1:
      days+=0
    elif final_m==2:
      days+=31
    elif final_m==3:
      days+=59
    elif final_m==4:
      days+=90
    elif final_m==5:
      days+=120
    elif final_m==6:
      days+=  151
    elif final_m==7:
      days+=181
    elif final_m==8:
      days+=212
    elif final_m==9:
      days+=243
    elif final_m==10:
      days+=273
    elif final_m==11:
      days+=304

  total_final = (days * 24) - (24-final_h)
  if final_a - inicial_a > 90:
    total_final = (days * 24) - (24 - final_h)



  END=abs(total_anos)+abs(total_inicial)+abs(total_final)
  print(f"Total de horas vividas: {END}")



main()