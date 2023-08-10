"use client"
import React, { useState, useEffect } from 'react';
import Link from 'next/link';

function Home() {
  const [markets, setMarkets] = useState([]);

  useEffect(() => {
    async function fetchMarkets() {
      try {
        const response = await fetch('http://localhost:8000/api/markets/');
        const data = await response.json();
        setMarkets(data['results']);
      } catch (error) {
        console.error('Error fetching markets:', error);
      }
    }

    fetchMarkets();
  }, []);


  const triggerRedirect = (id) => {
    console.log(id)
  }

  return (
    <div className=" min-h-screen py-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Markets</h1>
        <table className="w-full  shadow-md rounded-md">
          <thead>
            <tr className="">
              <th className="p-4">ID</th>
              <th className="p-4">Name</th>
            </tr>
          </thead>
          <tbody>
            {markets.map((market) => (
              <tr
                key={market.id}
                className="hover:bg-slate-800	 transition-colors"
                onClick={() => { triggerRedirect(market.id) }}
              >
                <td className="p-4">{market.id}</td>
                <td className="p-4">
                  <div className="hover:underline">{market.name}</div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Home;
