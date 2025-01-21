import React from "react";

const GameCard = () => {
  return (
    <div className="w-full">
      <table className="w-full table-auto text-left">
        <tr>
          <th className="py-4"> School </th>
          <th className="p-4"> Player </th>
          <th className="p-4"> Score </th>
          <th className="p-4"> Goals </th>
          <th className="p-4"> Assists </th>
          <th className="p-4"> Shots </th>
          <th className="py-4"> Saves </th>
        </tr>

        <tr>
          <td className="py-4"> Colorado College </td>
          <td className="p-4"> Sir James </td>
          <td className="p-4"> 100 </td>
          <td className="p-4"> 213</td>
          <td className="p-4"> 232 </td>
          <td className="p-4"> 213</td>
          <td className="py-4"> 23321 </td>
        </tr>
      </table>
    </div>
  );
};

export default GameCard;
