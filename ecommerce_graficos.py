from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("C:/Users/kikot/Downloads/ecommerce_preparados.csv")
# ver as colunas
print(df.columns)
# Verificando o tipo de dado de cada coluna
print(df.dtypes)


#1 Gráfico de Histograma - Quantidade produtos pelo preco
plt.figure(figsize=(8, 5))
sns.histplot(df['Preço'], bins='auto', kde=True) #kde para adicionar uma curva suave
plt.xlabel('Preço')
plt.ylabel('Frequência')
plt.title('Distribuição de Preço')
plt.show()

#2 Gráfico de dispersão - Para ver se descontos impulsionam vendas
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df['Preço'], y=df['Qtd_Vendidos'], alpha=0.5)
plt.xlabel("Preço (R$)")
plt.ylabel("Quantidade Vendida")
plt.title("Relação entre Preço e Quantidade Vendida")
plt.show()

#3 Mapa de calor
colunas_numericas = ['Nota', 'N_Avaliações', 'Desconto', 'Preço', 'Nota_MinMax',
                     'N_Avaliações_MinMax', 'Desconto_MinMax', 'Preço_MinMax']  # Selecionando apenas as colunas numéricas
correlacao = df[colunas_numericas].corr() # Calcular a correlação entre as colunas numéricas

                           # Criar o mapa de calor
plt.figure(figsize=(10, 8))
sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
plt.title("Mapa de Calor da Correlação entre Variáveis")
plt.show()

#4 Gráfico de barra
df_bar = df.groupby('Marca', as_index=False)['Preço'].mean() # Remover valores nulos e calcular a média de preço por marca
df_bar = df_bar.sort_values(by='Preço', ascending=False)  # Ordenar do maior para o menor preço
df_bar = df_bar.head(30)  # Mantém apenas as 30 marcas com maior preço médio


                            # Criar o gráfico de barras
plt.figure(figsize=(12, 6))
sns.barplot(x='Marca', y='Preço', data=df_bar, palette='viridis', legend=False)
plt.xticks(rotation=45,  ha='right')  # Rotaciona e alinha os nomes das marcas
plt.xlabel('Marca')
plt.ylabel('Preço Médio (R$)')
plt.title('Média de Preço por Marca')

                  # Aumentar espaço inferior para melhorar a visibilidade dos rótulos
plt.subplots_adjust(bottom=0.30)
plt.show()


#5 Gráfico de pizza
df_pizza = df['Gênero'].value_counts()
df_pizza = df_pizza[df_pizza / df_pizza.sum() >= 0.05]   # Filtra se a porcentagem for maior ou igual a 5%


                          # Criar o gráfico de pizza
plt.figure(figsize=(8, 8))
colors = sns.color_palette("Pastel1", len(df_pizza))
plt.pie(df_pizza, labels=df_pizza.index, autopct='%1.1f%%', colors=colors, wedgeprops={'edgecolor': 'black'})
plt.title('Distribuição de Produtos por Gênero')
plt.show()


#6 Gráfico de densidade
plt.figure(figsize=(10, 6))
sns.kdeplot(df['Preço'], fill=True, color='blue', linewidth=2, label='Preço')   # Plot para preço
plt.title("Distribuição de Preço", fontsize=16)
plt.xlabel('Preço', fontsize=12)
plt.ylabel('Densidade', fontsize=12)
plt.grid(True)
plt.show()


#7 Gráfico de Regressão

                    # Função para converter 'Qtd_Vendidos' de string para número
def converter_qtd_vendidos(valor):
    try:
        # Se for string com 'mil', converte para número
        if 'mil' in valor:
            return float(valor.replace('mil', '').strip()) * 1000  # Converte de mil para número
        return float(valor)  # Tenta converter para float normalmente
    except ValueError:
        # Se não for possível converter (ex: 'Nenhum', 'Desconhecido'), substitui por 0
        return 0

df['Qtd_Vendidos'] = df['Qtd_Vendidos'].fillna('0').apply(converter_qtd_vendidos) # Aplicar a conversão na coluna 'Qtd_Vendidos'
plt.figure(figsize=(10, 6))
sns.regplot(x='Preço', y='Qtd_Vendidos',data=df, scatter_kws={'color':'blue', 'alpha':0.5}, line_kws={'color': 'red'})
plt.title("Relação entre Preço e Quantidade Vendida", fontsize=16)
plt.xlabel("Preço", fontsize=12)
plt.ylabel("Quantidade Vendida", fontsize=12)
plt.show()


