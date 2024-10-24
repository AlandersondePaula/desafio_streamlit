# Streamlit
import locale
from datetime import datetime

import numpy as np

# Analise de Dados
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
from streamlit_option_menu import option_menu  # menu para sidebar do streamlit

#######################
# Carregando arquivos
#######################
df = pd.read_parquet('./dados_energia.parquet')

df_corrente = df[['Corrente Fase A', 'Corrente Fase B',
                  'Corrente Fase C', 'Corrente de Neutro']]
df_potencia = df[[
    'Potencia Ativa(P)', 'Potencia Reativa(Q)', 'Potencia Aparente(S)']]
df_tensao = df[['Tensao Fase A', 'Tensao Fase B', 'Tensao Fase C']]

meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
         "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

dicio_dias = {1: "Seg", 2: "Ter", 3: "Qua",
              4: "Qui", 5: "Sex", 6: "Sab", 7: "Dom"}

opcoes_corrente = dict([('Corrente Fase A', 1), ('Corrente Fase B', 2),
                       ('Corrente Fase C', 3)])
opcoes_potencia = dict([('Potência Ativa(P)', 1),
                       ('Potência  Reativa(Q)', 2), ('Potência Aparente(S)', 3)])
opcoes_tensao = dict(
    [('Tensão Fase A', 1), ('Tensão Fase B', 2), ('Tensão Fase C', 3)])

# obtém uma lista de números de meses únicos a partir do DataFrame
meses_unicos = df['Data'].dt.month.unique().tolist()
meses_unicos.sort()

df['dia_da_semana'] = df['Data'].dt.dayofweek + 1
df['nome_dia_semana'] = df['dia_da_semana'].map(dicio_dias)

anos_unicos = df['Data'].dt.year.unique().tolist()
dias_unicos = df['Data'].dt.day.unique().tolist()


def atualiza_grafico(selecao1: str = 'Janeiro', selecao2: int = 2022, selecao6: int = 0, selecao3: int = 0, selecao4: int = 0, selecao5: int = 0) -> None:
    """
    Plota um gráfico com base em uma seleção de colunas e meses de um dataframe.

    Parâmetros:
    ----------

    `selecao1 (str)`: O nome do mês que se deseja selecionar. Exemplo: 'Janeiro'
    `selecao2 (int)`: O ano que se deseja selecionar. Exemplo: 2022
    `selecao3 (int)`: A coluna que se deseja selecionar para o eixo y1 do gráfico.
    `selecao4 (int)`: A coluna que se deseja selecionar para o eixo y3 do gráfico.
    `selecao5 (int)`: A coluna que se deseja selecionar para o eixo y4 do gráfico.

    Retorno:
    ---------

    `None`: A função plota um gráfico interativo do pacote Plotly.
    """
    nome_dia = pd.DataFrame()
    filtro_df = df[(df['Data'].dt.month == meses.index(selecao1) + 1) &
                   (df['Data'].dt.year == selecao2) & (df['Data'].dt.day == selecao6)]
    # df_filtrado = df[df['Data'].dt.day == selecao6]
    if not filtro_df.empty:
        nome_dia = filtro_df.iloc[0]['nome_dia_semana']

    coluna = df_corrente.columns[selecao3-1]
    coluna2 = df_potencia.columns[selecao4-1]
    coluna3 = df_tensao.columns[selecao5-1]

    dic_opcoes_corrente = dict([(1, 'Corrente Fase A'), (2, 'Corrente Fase B'),
                               (3, 'Corrente Fase C'), (4, 'Corrente de Neutro')])
    dic_opcoes_potencia = dict(
        [(1, 'Potência Ativa(P)'), (2, 'Potência  Reativa(Q)'), (3, 'Potência Aparente(S)')])
    dic_opcoes_tensao = dict(
        [(1, 'Tensão Fase A'), (2, 'Tensão Fase B'), (3, 'Tensão Fase C')])

    y1 = filtro_df[coluna]
    y2 = filtro_df[coluna2]
    y3 = filtro_df[coluna3]
    y4 = filtro_df['Data']
    y5 = filtro_df['Fator de Potencia(FP)']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df[coluna],
        name=dic_opcoes_corrente[selecao3],
        yaxis='y1'
    ))

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df[coluna2],
        name=dic_opcoes_potencia[selecao4],
        yaxis='y2'
    ))

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df[coluna3],
        name=dic_opcoes_tensao[selecao5],
        yaxis='y3'
    ))

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Corrente de Neutro'],
        name='Corrente de Neutro',
        yaxis='y4',
    ))

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Fator de Potencia(FP)'],
        name='Fator de Potência(FP)',
        yaxis='y5',
    ))

    fig.update_layout(

        yaxis=dict(
            titlefont={"color": 'green'},
            tickfont={"color": 'green'},
            side='left',
            range=[-225, 370],
        ),

        yaxis2=dict(
            # title = 'Data',
            titlefont={"color": 'black'},
            tickfont={"color": 'black'},
            overlaying='y',
            side='right',
            showticklabels=False,
            range=[-225, 370]
        ),

        yaxis3=dict(
            # title = 'Data',
            titlefont={"color": 'green'},
            tickfont={"color": 'green'},
            overlaying='y',
            side='right',
            range=[220, 240],
        ),

        yaxis4=dict(
            # title = 'Data',
            titlefont={"color": 'purple'},
            tickfont={"color": 'purple'},
            overlaying='y',
            side='right',
            showticklabels=False,
            range=[-225, 370],
        ),

        yaxis5=dict(
            titlefont={"color": 'black'},
            tickfont={"color": 'black'},
            overlaying='y',
            side='right',
            range=[0, 1],
        ),

        autosize=False,
        width=1200,
        height=400,
        margin={"l": 10, "r": 10, "b": 10, "t": 35, "pad": 50},

        legend={"orientation": 'h', "yanchor": 'top',
                "y": 1, "xanchor": 'left', "x": 0.01},

        title=f'{selecao6} de {selecao1}/{selecao2}',
        title_x=0.4,
        xaxis_tickformat=f'%d {selecao1} ({nome_dia})<br>%Y - %H:%M:%S',

    )

    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='black', tickangle=45)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

    return fig


def atualiza_grafico_tensao(selecao1: str = 'Janeiro', selecao2: int = 2022, selecao3: int = 0) -> None:

    nome_dia = pd.DataFrame()
    filtro_df = df[(df['Data'].dt.month == meses.index(selecao1) + 1) &
                   (df['Data'].dt.year == selecao2) & (df['Data'].dt.day == selecao3)]
    if not filtro_df.empty:
        nome_dia = filtro_df.iloc[0]['nome_dia_semana']

    y1 = filtro_df['Tensao Fase A']
    y2 = filtro_df['Tensao Fase B']
    y3 = filtro_df['Tensao Fase C']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Tensao Fase A'],
        name='Tensao Fase A',
        yaxis='y1'
    ))

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Tensao Fase B'],
        name='Tensao Fase B',
        yaxis='y2'
    ))

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Tensao Fase C'],
        name='Tensao Fase C',
        yaxis='y3'
    ))

    fig.update_layout(

        yaxis=dict(
            titlefont={"color": 'green'},
            tickfont={"color": 'green'},
            side='left',
            range=[220, 240]
        ),

        yaxis2=dict(
            # title = 'Data',
            overlaying='y',
            side='right',
            showticklabels=False,
            range=[220, 240]
        ),

        yaxis3=dict(
            # title = 'Data',
            titlefont={"color": 'green'},
            tickfont={"color": 'green'},
            overlaying='y',
            side='right',
            range=[220, 240],
        ),

        autosize=False,
        width=1200,
        height=400,
        margin={"l": 10, "r": 10, "b": 10, "t": 35, "pad": 50},

        legend={"orientation": 'h', "yanchor": 'top',
                "y": 1, "xanchor": 'left', "x": 0.01},

        title=f'Visualização do gráfico de Tensão do dia {selecao3} de {selecao1}/{selecao2}',
        title_x=0.2,
        xaxis_tickformat=f'%d {selecao1} ({nome_dia})<br>%Y - %H:%M:%S',

    )

    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='black', tickangle=45)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
    return fig


def atualiza_grafico_corrente(selecao1: str = 'Janeiro', selecao2: int = 2022, selecao3: int = 0) -> None:

    nome_dia = pd.DataFrame()
    filtro_df = df[(df['Data'].dt.month == meses.index(selecao1) + 1) &
                   (df['Data'].dt.year == selecao2) & (df['Data'].dt.day == selecao3)]
    if not filtro_df.empty:
        nome_dia = filtro_df.iloc[0]['nome_dia_semana']

    y1 = filtro_df['Corrente Fase A']
    y2 = filtro_df['Corrente Fase B']
    y3 = filtro_df['Corrente Fase C']
    y4 = filtro_df['Corrente de Neutro']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Corrente Fase A'],
        name='Corrente Fase A',
        yaxis='y1'
    ))

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Corrente Fase B'],
        name='Corrente Fase B',
        yaxis='y2'
    ))

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Corrente Fase C'],
        name='Corrente Fase C',
        yaxis='y3'
    ))

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Corrente de Neutro'],
        name='Corrente de Neutro',
        yaxis='y4'
    ))

    fig.update_layout(

        yaxis=dict(
            titlefont={"color": 'green'},
            tickfont={"color": 'green'},
            # side='left',
            side='right',
            range=[0, 450]
        ),

        yaxis2=dict(
            # title = 'Data',
            overlaying='y',
            side='right',
            showticklabels=False,
            range=[0, 450]
        ),

        yaxis3=dict(
            # title = 'Data',
            titlefont={"color": 'green'},
            tickfont={"color": 'green'},
            overlaying='y',
            side='right',
            range=[0, 450],
        ),

        yaxis4=dict(
            # title = 'Data',
            titlefont={"color": 'green'},
            tickfont={"color": 'green'},
            overlaying='y',
            side='left',
            range=[0, 100],
        ),

        autosize=False,
        width=1200,
        height=400,
        margin={"l": 10, "r": 10, "b": 10, "t": 35, "pad": 50},

        legend={"orientation": 'h', "yanchor": 'top',
                "y": 1, "xanchor": 'left', "x": 0.01},

        title=f'Visualização do gráfico de Corrente do dia {selecao3} de {selecao1}/{selecao2}',
        title_x=0.2,
        xaxis_tickformat=f'%d {selecao1} ({nome_dia})<br>%Y - %H:%M:%S',


    )

    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='black', tickangle=45)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
    return fig


def atualiza_grafico_potencia(selecao1: str = 'Janeiro', selecao2: int = 2022, selecao3: int = 0) -> None:

    nome_dia = pd.DataFrame()
    filtro_df = df[(df['Data'].dt.month == meses.index(selecao1) + 1) &
                   (df['Data'].dt.year == selecao2) & (df['Data'].dt.day == selecao3)]
    if not filtro_df.empty:
        nome_dia = filtro_df.iloc[0]['nome_dia_semana']

    y1 = filtro_df['Potencia Ativa(P)']
    y2 = filtro_df['Potencia Reativa(Q)']
    y3 = filtro_df['Potencia Aparente(S)']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Potencia Ativa(P)'],
        name='Potencia Ativa(P)',
        yaxis='y1'
    ))

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Potencia Reativa(Q)'],
        name='Potencia Reativa(Q)',
        yaxis='y2'
    ))

    fig.add_trace(go.Scatter(
        x=filtro_df['Data'],
        y=filtro_df['Potencia Aparente(S)'],
        name='Potencia Aparente(S)',
        yaxis='y3'
    ))

    fig.update_layout(

        yaxis=dict(
            titlefont={"color": 'green'},
            tickfont={"color": 'green'},
            side='left',
            range=[-225, 250]
        ),

        yaxis2=dict(
            # title = 'Data',
            overlaying='y',
            side='right',
            showticklabels=False,
            range=[-225, 250]
        ),

        yaxis3=dict(
            # title = 'Data',
            titlefont={"color": 'green'},
            tickfont={"color": 'green'},
            overlaying='y',
            side='right',
            range=[-225, 250],
        ),

        autosize=False,
        width=1200,
        height=400,
        margin={"l": 10, "r": 10, "b": 10, "t": 35, "pad": 50},

        legend={"orientation": 'h', "yanchor": 'top',
                "y": 1, "xanchor": 'left', "x": 0.01},
        title=f'Visualização do gráfico de Potência do dia {selecao3} de {selecao1}/{selecao2}',
        title_x=0.2,
        xaxis_tickformat=f'%d {selecao1} ({nome_dia})<br>%Y - %H:%M:%S',

    )

    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='black', tickangle=45)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
    return fig

### ### ### ###
### front-end ###
### ### ### ###


# Titulo - subtitulo
st.set_page_config(
    page_title='Processo Seletivo',
    page_icon='📊',
    layout='wide'
)

### Sidebar Superior ###
st.sidebar.image('./logo_hvex1.png')
st.sidebar.title('Processo')

# customizar a sidebar
with st.sidebar:

    # menu de seleção
    selected = option_menu(

        # titulo
        'Menu',

        # opções de navegação
        ['Corrente', 'Potência', 'Tensão', 'Dashboard'],

        # Icones para o menu das opções
        icons=['bar-chart-fill', 'bar-chart-fill',
               'bar-chart-fill', 'bar-chart-fill'],

        # icone do menu principal
        menu_icon='cast',

        # Seleção padrão
        default_index=0,

        # Estilos
        styles={
            # Diminui o tamanho da fonte do título
            'menu-title': {'font-size': '24px'},
            'menu-icon': {'display': 'none'},  # Remove o ícone do título
            'icon': {'font-size': '12px'},  # Estilo dos ícones
            'nav-link': {
                'font-size': '15px',  # Tamanho da fonte dos itens do menu
                '--hover-color': '#6052d9',  # Cor de fundo ao passar o mouse
            },
            # Cor de fundo do item selecionado
            'nav-link-selected': {'background-color': '#157806'},
        }
    )

# Navegação das paginas
if selected == 'Dashboard':

    # Tabela
    col1, col2, col3, col4, col5 = st.columns([0.1, 0.2, 0.2, 0.2, 0.2])

    with col1:
        selecione_dia = st.selectbox('Dia', dias_unicos)

    with col2:
        selecione_corrente = st.selectbox('Corrente', opcoes_corrente.keys())

    with col3:
        selecione_potencia = st.selectbox('Potência', opcoes_potencia.keys())

    with col4:
        selecione_tensao = st.selectbox('Tensão', opcoes_tensao.keys())

    chamar_grafico = atualiza_grafico(
        selecao6=selecione_dia, selecao3=opcoes_corrente[selecione_corrente], selecao4=opcoes_potencia[selecione_potencia], selecao5=opcoes_tensao[selecione_tensao])

    st.plotly_chart(chamar_grafico)

    # rodapé
    st.markdown(
        '''
            <hr style='border: 1px solid #d3d3d3;'/>
            <p style='text-align: center; color: gray;'>
                Dashboard de Análise de Energia | Dados fornecidos por HVex | Desenvolvido por Alanderson Tadeu de Paula | © 2024
            </p>
        ''',
        unsafe_allow_html=True
    )

elif selected == 'Tensão':

    col1, col2 = st.columns([0.1, 0.9])

    with col1:
        selecione_dia_tensao = st.selectbox('Dia', dias_unicos)

    chamar_grafico1 = atualiza_grafico_tensao(
        selecao3=selecione_dia_tensao)

    st.plotly_chart(chamar_grafico1)

    # rodapé
    st.markdown(
        '''
            <hr style='border: 1px solid #d3d3d3;'/>
            <p style='text-align: center; color: gray;'>
                Dashboard de Análise de Energia | Dados fornecidos por HVex | Desenvolvido por Alanderson Tadeu de Paula | © 2024
            </p>
        ''',
        unsafe_allow_html=True

    )

elif selected == 'Potência':

    col1, col2 = st.columns([0.1, 0.9])

    with col1:
        selecione_dia_potencia = st.selectbox('Dia', dias_unicos)

    chamar_grafico2 = atualiza_grafico_potencia(
        selecao3=selecione_dia_potencia)

    st.plotly_chart(chamar_grafico2)

    # rodapé
    st.markdown(
        '''
            <hr style='border: 1px solid #d3d3d3;'/>
            <p style='text-align: center; color: gray;'>
                Dashboard de Análise de Energia | Dados fornecidos por HVex | Desenvolvido por Alanderson Tadeu de Paula | © 2024
            </p>
        ''',
        unsafe_allow_html=True

    )

elif selected == 'Corrente':

    col1, col2 = st.columns([0.1, 0.9])

    with col1:
        selecione_dia_corrente = st.selectbox('Dia', dias_unicos)

    chamar_grafico3 = atualiza_grafico_corrente(
        selecao3=selecione_dia_corrente)

    st.plotly_chart(chamar_grafico3)

    # rodapé
    st.markdown(
        '''
            <hr style='border: 1px solid #d3d3d3;'/>
            <p style='text-align: center; color: gray;'>
                Dashboard de Análise de Energia | Dados fornecidos por HVex | Desenvolvido por Alanderson Tadeu de Paula | © 2024
            </p>
        ''',
        unsafe_allow_html=True

    )

else:
    pass
