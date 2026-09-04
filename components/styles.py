import streamlit as st


def load_css():

    st.markdown("""
    <style>

    .main-title{
        font-size:40px;
        font-weight:700;
        color:#0066B3;
        margin-bottom:20px;
    }

    .section-title{
        background:#6E6E6E;
        color:white;
        text-align:center;
        font-size:22px;
        font-weight:boldPerfeito. Para deixar os **cards dos SKUs centralizados**, com imagem, SKU e preços alinhados visualmente, substitua o conteúdo do seu `components/styles.py` por este:

```python
import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* TÍTULO PRINCIPAL */

    .main-title{
        font-s*ze:40px;
        font-weight:700;
*       color:#0066B3;
        marg*n-bottom:20px;
*   }

    /* TÍTULOS DAS SEÇÕES */

    .section-title{
        ba*kground:#6E6E*E;
        color:white;
        te*t-align:center*
*       font-size:22px;
        fon*-weight:bold;
        border-radiu*:5px;
        padding:8px;
        margin-bottom:10px;
    }

    /* MECÂNICA */

    .mecanica-box{
  *     background:white;
        bor*er:1px solid #CFCFC*;
        border-radius:8px;
     *  padding:15px;
        min*height:250px;
*       color:black;
    }

    .me*anica-subtitle{
        background*#E8E8E*;
        color*black;
        text-align:center;
*       font-weight:bold;
       *padding*8px;
        border-radius:5*x;
        margin-top:10px;
      * margin-bottom:10px*
    }

    .mecanica-lista{
     *  padding-left:*0px;
        margin-bottom:15px;
*   }

    .mecanica-lista li{
*       margin-bottom:8px;
        *olor:black;
*   }

    /* TÍTULOS DOS CANAIS */

    .canal-title{
        backg*ound:#6E6E6E;
*       color:white;
        text-a*ign:center;
        font*size:24px;
        font-weight:bol*;
        border-radius:5px;
     *  padding:10px;
        margin-top*20px;
        margin-bottom:15px;
*   }

    /* QUINZENAS */

    .quinzena-title{
        ba*kground:#*8*8E8;
        color:black;
        *ext-align:center;
        font-siz*:18px;
        font-weight:bold;
 *      border-radius:5px;
        p*dding:8px;
        margin-top:10px;
        margin-bottom:15px;
    }

    /* CARD DO PRODUTO */

    .produto*card{
        text-align:center;
 *      padding:10px;
        margin*bottom:15px;
*   }

    /* SKU */

    .sku-name{
        text-ali*n:center;
        font-size:14px;
*       font-weight:bold;
        c*lor:black;
        margin-top:8px;*        margin-bottom:8px;
       *min-height:35px;
    }

    /* PREÇO DE */

    .old-price{
        backgro*nd:#6E6E6E;
        color:white;
*       text-align:center;
        *order-radius:20px;
        padding*6px;
        width:80%;
        ma*gin:5px auto;
        font-size:13px;
    }

    /* PREÇO PARA */

    .new-price{
        backgr*und:#B3B3B*;
        color:white;
        tex*-align:center;
        border*radius:20px;
*       padding:6px;
        width:*0%;
        margin:5px auto;
     *  font-size:13px;
        font-weight:bold;
    }

    /* CENTRALIZA TODAS AS IMAGENS DOS PRODUTOS */

    [data-testid="stImage"]{
  *     text*align:center;
    }

    </*tyle>
    """,*unsafe_allow_html=True)
