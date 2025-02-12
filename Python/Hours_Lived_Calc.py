def main():   #vou ter q converter o possível 02 pra 2
  END=0 #valor final
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

  meses=[1,2,3,4,5,6,7,8,9,10,11,12]
  days=0
  years=0
  leap=0
  month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}



  for i in range(inicial_a, final_a+1):
    years += 1
    print(i)
    if i % 4 == 0:
      if i % 100 > 0:
        bissexto = 1
      else:
        if i % 400 == 0:
          bissexto += 1

  years=(ano + bissexto) * 8760
  print(years)

  def mes():
    for i in range(month[final_m] + 1):
      i += 1
      if i == final_d:
        i *= 24
        return i

  def mes2():
    for j in range(month[final_m] + 1):
      j += 1
      if j == inicial_d:
        j *= 24
        return j

  days=mes()-mes2()


  def mestrue():
    interval = (final_m-1)- inicial_m
    if interval>0:
      for z in range(interval):
        z += month[z]
      z +=24
      
      return z
  #need to fix this, some variable error 


  END=years+days+month

main()
