import streamlit as st
import pandas as pd
from typing import List, Dict

# Initialize session state
if 'participants' not in st.session_state:
    st.session_state.participants = [
        {"name": "Person 1", "paid": 0.0},
        {"name": "Person 2", "paid": 0.0}
    ]

def format_rupee(amount: float) -> str:
    """Format amount as Indian Rupees with proper locale formatting"""
    return f"₹{amount:,.2f}"

def add_participant():
    """Add a new participant with default name based on current count"""
    new_idx = len(st.session_state.participants) + 1
    st.session_state.participants.append({
        "name": f"Person {new_idx}",
        "paid": 0.0
    })

def remove_participant(idx: int):
    """Remove participant at given index with safety check"""
    if len(st.session_state.participants) > 1:  # Always keep at least one
        del st.session_state.participants[idx]
    else:
        st.warning("⚠️ Cannot remove the last participant!")

def main():
    st.set_page_config(
        page_title="💰 Rupee Expense Splitter",
        page_icon="💸",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title("💸Expense Splitter")
    st.markdown("Split expenses fairly among friends in Indian Rupees")

    # Total cost input with Rupee formatting
    st.subheader("🛒 Total Expense")
    total_cost = st.number_input(
        f"Total amount spent ({format_rupee(0)})", 
        min_value=0.0,
        value=0.0,
        step=10.0,
        format="%.2f",
        key="total_cost"
    )
    
    # Dynamic participant management
    st.subheader("👥 Manage Participants")
    with st.expander("Add or remove participants", expanded=True):
        # Add participant button with Rupee context
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("➕ Add Person", use_container_width=True):
                add_participant()
                st.rerun()
        
        # Display current participants
        for idx, participant in enumerate(st.session_state.participants):
            with st.container():
                cols = st.columns([3, 2, 1])
                with cols[0]:
                    name = st.text_input(
                        "Name",
                        value=participant["name"],
                        key=f"name_{idx}",
                        label_visibility="collapsed"
                    )
                    st.session_state.participants[idx]["name"] = name
                
                with cols[1]:
                    paid = st.number_input(
                        f"Paid ({format_rupee(0)})",
                        min_value=0.0,
                        value=float(participant["paid"]),
                        step=10.0,
                        format="%.2f",
                        key=f"paid_{idx}",
                        label_visibility="collapsed"
                    )
                    st.session_state.participants[idx]["paid"] = paid
                
                with cols[2]:
                    if st.button("🗑️", key=f"del_{idx}", help="Remove participant"):
                        remove_participant(idx)
                        st.rerun()
    
    # Calculate button with Rupee context
    if st.button(f"🧮 Calculate Split ({format_rupee(total_cost)} Total)", 
                type="primary", 
                use_container_width=True,
                disabled=(total_cost <= 0 or len(st.session_state.participants) == 0)):
        
        # Validation checks
        if total_cost <= 0:
            st.error("❌ Total expense must be greater than zero")
            st.stop()
            
        if len(st.session_state.participants) == 0:
            st.error("❌ Add at least one participant")
            st.stop()
        
        # Get current participant data
        participants = st.session_state.participants.copy()
        total_paid = sum(p["paid"] for p in participants)
        num_people = len(participants)
        
        # Fair share calculation
        fair_share = total_cost / num_people
        
        # Calculate balances (positive = needs to pay, negative = should receive)
        results = []
        for p in participants:
            balance = fair_share - p["paid"]
            status = "✅ Exact" if abs(balance) < 0.01 else \
                     "🟩 Receives" if balance < 0 else \
                     "🟥 Pays"
            amount = abs(balance)
            
            results.append({
                "Person": p["name"],
                "Paid": format_rupee(p["paid"]),
                "Fair Share": format_rupee(fair_share),
                "Status": status,
                "Amount": format_rupee(amount) if amount >= 0.01 else "₹0.00"
            })
        
        # Display results
        st.subheader("📊 Split Results")
        results_df = pd.DataFrame(results)
        
        # Style the dataframe
        def color_status(val):
            if "Receives" in val:
                return 'background-color: #d4edda; color: #155724'
            elif "Pays" in val:
                return 'background-color: #f8d7da; color: #721c24'
            return 'background-color: #d1ecf1; color: #0c5460'
        
        st.dataframe(
            results_df.style.applymap(color_status, subset=['Status']),
            use_container_width=True,
            hide_index=True
        )
        
        # Settlement instructions
        st.subheader("🧾 Settlement Instructions")
        
        # Prepare for settlement calculations
        creditors = []  # People who should receive money (balance < 0)
        debtors = []    # People who need to pay (balance > 0)
        
        for p in participants:
            balance = fair_share - p["paid"]
            if balance < -0.01:  # Should receive money
                creditors.append((p["name"], abs(balance)))
            elif balance > 0.01:  # Needs to pay
                debtors.append((p["name"], balance))
        
        # Generate settlement transactions
        transactions = []
        creditor_idx = debtor_idx = 0
        
        while creditor_idx < len(creditors) and debtor_idx < len(debtors):
            creditor, credit_amt = creditors[creditor_idx]
            debtor, debt_amt = debtors[debtor_idx]
            
            transfer_amt = min(credit_amt, debt_amt)
            if transfer_amt >= 0.01:  # Meaningful amount
                transactions.append((debtor, creditor, transfer_amt))
            
            creditors[creditor_idx] = (creditor, credit_amt - transfer_amt)
            debtors[debtor_idx] = (debtor, debt_amt - transfer_amt)
            
            if credit_amt - transfer_amt < 0.01:
                creditor_idx += 1
            if debt_amt - transfer_amt < 0.01:
                debtor_idx += 1
        
        # Display settlement
        if not transactions:
            st.success("🎉 Everyone has paid exactly their fair share!")
        else:
            st.write("Make these payments to settle up:")
            for debtor, creditor, amount in transactions:
                st.markdown(
                    f"- **{debtor}** pays **{format_rupee(amount)}** to **{creditor}**"
                )
            
            # Settlement summary
            st.caption("💡 Pro Tip: Use UPI apps like PhonePe, Google Pay, or Paytm for instant settlements")

if __name__ == "__main__":
    main()