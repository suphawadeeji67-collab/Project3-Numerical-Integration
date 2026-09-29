import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# PAGE SETUP
# ==========================================

st.set_page_config(
    page_title="Project 3 - Numerical Integration",
    page_icon="📐",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("Project 3#")
st.subheader("Comparison of Numerical Integration Approximations")

st.markdown(
    "### ประมาณค่า "
    r"$A=\int_a^b(1+e^x)\,dx$"
)

st.divider()


# ==========================================
# FUNCTION
# ==========================================

def f(x):
    return 1 + np.exp(x)


# ==========================================
# EXACT VALUE
# ==========================================

def exact_integral(a, b):
    return (b - a) + np.exp(b) - np.exp(a)


# ==========================================
# TRAPEZOIDAL
# ==========================================

def trapezoidal(a, b, n):

    h = (b - a) / n

    x = np.linspace(a, b, n + 1)
    y = f(x)

    result = h * (
        (y[0] + y[-1]) / 2
        + np.sum(y[1:-1])
    )

    return result, h, x, y


# ==========================================
# SIMPSON
# ==========================================

def simpson(a, b, n):

    if n % 2 != 0:
        return None, None, None, None

    h = (b - a) / n

    x = np.linspace(a, b, n + 1)
    y = f(x)

    result = (h / 3) * (
        y[0]
        + y[-1]
        + 4 * np.sum(y[1:-1:2])
        + 2 * np.sum(y[2:-1:2])
    )

    return result, h, x, y


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("⚙️ Input Parameters")

a = st.sidebar.number_input(
    "กำหนดค่า a",
    value=0.0
)

b = st.sidebar.number_input(
    "กำหนดค่า b",
    value=1.0
)

n = st.sidebar.selectbox(
    "กำหนดค่า n",
    [8, 16, 32, 64]
)

method = st.sidebar.selectbox(
    "เลือกวิธีการคำนวณ",
    [
        "เปรียบเทียบทั้ง 2 วิธี",
        "Trapezoidal",
        "Simpson's"
    ]
)


# ==========================================
# CHECK
# ==========================================

if b <= a:

    st.error("กรุณากำหนด b > a")

    st.stop()


# ==========================================
# CALCULATE
# ==========================================

A = exact_integral(a, b)

trap_value, h, x, y = trapezoidal(
    a, b, n
)

simp_value, _, _, _ = simpson(
    a, b, n
)

trap_error = abs(A - trap_value)

simp_error = abs(A - simp_value)


# ==========================================
# 1. INPUT
# ==========================================

st.header("1. Input")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("a", f"{a:.6f}")

with col2:
    st.metric("b", f"{b:.6f}")

with col3:
    st.metric("n", n)


# ==========================================
# 2. MATHEMATICAL NOTATION
# ==========================================

st.header("2. Mathematical Notation")

st.latex(
    r"""
    A=\int_a^b(1+e^x)\,dx
    """
)

st.latex(
    r"""
    A=(b-a)+e^b-e^a
    """
)

st.write(
    f"ค่าจริงของ A = **{A:.10f}**"
)


# ==========================================
# 3. RESULTS
# ==========================================

st.header("3. Results")

if method == "เปรียบเทียบทั้ง 2 วิธี":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Exact A",
            f"{A:.6f}"
        )

    with col2:
        st.metric(
            "Trapezoidal",
            f"{trap_value:.6f}"
        )

    with col3:
        st.metric(
            "Simpson's",
            f"{simp_value:.6f}"
        )

    st.markdown("### Error")

    col1, col2 = st.columns(2)

    with col1:
        st.write(
            f"Trapezoidal Error = "
            f"**{trap_error:.6e}**"
        )

    with col2:
        st.write(
            f"Simpson's Error = "
            f"**{simp_error:.6e}**"
        )

elif method == "Trapezoidal":

    st.metric(
        "Trapezoidal Approximation",
        f"{trap_value:.10f}"
    )

    st.write(
        f"Error = **{trap_error:.6e}**"
    )

else:

    st.metric(
        "Simpson's Approximation",
        f"{simp_value:.10f}"
    )

    st.write(
        f"Error = **{simp_error:.6e}**"
    )


# ==========================================
# 4. GRAPH
# ==========================================

st.header("4. Graph")

x_plot = np.linspace(a, b, 500)
y_plot = f(x_plot)

fig = go.Figure()

# Function
fig.add_trace(
    go.Scatter(
        x=x_plot,
        y=y_plot,
        mode="lines",
        name="f(x) = 1 + eˣ"
    )
)

# Area
fig.add_trace(
    go.Scatter(
        x=np.concatenate(
            ([a], x_plot, [b])
        ),
        y=np.concatenate(
            ([0], y_plot, [0])
        ),
        fill="toself",
        mode="none",
        name="Area"
    )
)

fig.update_layout(
    xaxis_title="x",
    yaxis_title="f(x)",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3 = st.tabs(
    [
        "Step-by-Step Calculation",
        "Error Table",
        "Comparison n = 64"
    ]
)


# ==========================================
# TAB 1
# ==========================================

with tab1:

    st.header("Step-by-Step Calculation")

    st.subheader("Trapezoidal Method")

    st.latex(
        r"""
        h=\frac{b-a}{n}
        """
    )

    st.write(
        f"h = ({b} - {a}) / {n}"
    )

    st.write(
        f"h = **{h:.10f}**"
    )

    st.latex(
        r"""
        T_n=h\left[
        \frac{f(a)+f(b)}{2}
        +\sum_{i=1}^{n-1}f(x_i)
        \right]
        """
    )

    st.write(
        f"Trapezoidal = **{trap_value:.10f}**"
    )

    st.write(
        f"Error = **{trap_error:.6e}**"
    )

    st.divider()

    st.subheader("Simpson's Method")

    st.latex(
        r"""
        S_n=\frac{h}{3}
        \left[
        f(x_0)+f(x_n)
        +4\sum f(x_{odd})
        +2\sum f(x_{even})
        \right]
        """
    )

    st.write(
        f"Simpson's = **{simp_value:.10f}**"
    )

    st.write(
        f"Error = **{simp_error:.6e}**"
    )


# ==========================================
# TAB 2
# ==========================================

with tab2:

    st.header("Error for n = 8, 16, 32, 64")

    n_values = [8, 16, 32, 64]

    data = []

    for ni in n_values:

        t, _, _, _ = trapezoidal(
            a, b, ni
        )

        s, _, _, _ = simpson(
            a, b, ni
        )

        error_t = abs(A - t)
        error_s = abs(A - s)

        data.append(
            [
                ni,
                error_t,
                error_s
            ]
        )

    df = pd.DataFrame(
        data,
        columns=[
            "n",
            "Trapezoidal Error",
            "Simpson Error"
        ]
    )

    st.dataframe(
        df.style.format(
            {
                "Trapezoidal Error": "{:.6e}",
                "Simpson Error": "{:.6e}"
            }
        ),
        use_container_width=True
    )


# ==========================================
# TAB 3
# ==========================================

with tab3:

    st.header("Comparison when n = 64")

    trap64, _, _, _ = trapezoidal(
        a, b, 64
    )

    simp64, _, _, _ = simpson(
        a, b, 64
    )

    error_t64 = abs(A - trap64)
    error_s64 = abs(A - simp64)

    comparison = pd.DataFrame(
        [
            [
                "Trapezoidal",
                A,
                trap64,
                error_t64
            ],
            [
                "Simpson",
                A,
                simp64,
                error_s64
            ]
        ],
        columns=[
            "Method",
            "A",
            "Approximation",
            "Error"
        ]
    )

    st.dataframe(
        comparison.style.format(
            {
                "A": "{:.6f}",
                "Approximation": "{:.6f}",
                "Error": "{:.6e}"
            }
        ),
        use_container_width=True
    )

    st.subheader("Output Format")

    st.code(
        f"""
Method          Approximation       Error
Trapezoidal     {trap64:.6f}         {error_t64:.5e}
Simpson         {simp64:.6f}         {error_s64:.5e}
"""
    )
