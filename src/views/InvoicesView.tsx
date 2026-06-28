import { useEffect, useState } from 'react';

export default function InvoicesView() {
  const [invoices, setInvoices] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/invoices')
      .then(res => res.ok ? res.json() : [])
      .then(setInvoices)
      .catch(console.error);
  }, []);

  const exportInvoice = (inv: any) => {
    const text = `
GRAND VISTA HOTEL - INVOICE
=================================
Invoice ID: ${inv.id}
Guest: ${inv.guest_name}
Check In: ${inv.check_in}
Check Out: ${inv.check_out}
---------------------------------
Subtotal: $${inv.subtotal.toFixed(2)}
Tax (10%): $${inv.tax.toFixed(2)}
=================================
TOTAL: $${inv.total.toFixed(2)}
    `;
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${inv.id}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {invoices.map(inv => (
          <div key={inv.id} className="bg-white dark:bg-gray-950 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm p-6 font-mono text-sm flex flex-col">
            <div className="flex justify-between items-start mb-6 pb-6 border-b border-gray-200 dark:border-gray-800">
              <div>
                <h3 className="font-bold text-lg mb-1">Grand Vista Hotel</h3>
                <p className="text-gray-500">Invoice: {inv.id}</p>
              </div>
              <button 
                onClick={() => exportInvoice(inv)}
                className="bg-gray-100 hover:bg-gray-200 dark:bg-gray-900 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300 px-3 py-1.5 rounded"
              >
                Export .txt
              </button>
            </div>
            
            <div className="space-y-2 mb-6">
              <div className="flex justify-between">
                <span className="text-gray-500">Guest</span>
                <span className="font-semibold">{inv.guest_name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Check In</span>
                <span>{inv.check_in}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Check Out</span>
                <span>{inv.check_out}</span>
              </div>
            </div>

            <div className="mt-auto pt-4 border-t border-gray-200 dark:border-gray-800 space-y-2">
              <div className="flex justify-between text-gray-500">
                <span>Subtotal</span>
                <span>${inv.subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-gray-500">
                <span>Tax (10%)</span>
                <span>${inv.tax.toFixed(2)}</span>
              </div>
              <div className="flex justify-between font-bold text-lg mt-2 pt-2 border-t border-gray-200 dark:border-gray-800 text-blue-600 dark:text-blue-400">
                <span>Total</span>
                <span>${inv.total.toFixed(2)}</span>
              </div>
            </div>
          </div>
        ))}
        
        {invoices.length === 0 && (
          <div className="col-span-full p-8 text-center text-gray-500 border border-dashed border-gray-300 dark:border-gray-700 rounded-xl">
            No invoices generated yet. Go to Bookings to generate an invoice.
          </div>
        )}
      </div>
    </div>
  );
}
