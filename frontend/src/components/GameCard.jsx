import React from "react";

const GameCard = (props) => {
  const { match, teamStats, opponentStats } = props;

  return (
    <div className="w-full p-8">
      <h3 className="p-4 text-center text-xl font-bold">
        {match.school +
          " " +
          match.teamScore +
          "-" +
          match.opponentScore +
          " " +
          match.opponent}
      </h3>

      <table className="w-full table-auto border border-black text-left">
        <tr className="border border-black">
          {Object.keys(teamStats[0]).map((header) => (
            <th className="border border-black p-4"> {header} </th>
          ))}
        </tr>

        {teamStats.map((player) => (
          <tr>
            {Object.values(player).map((stat) => (
              <td className="border-x border-black p-4"> {stat} </td>
            ))}
          </tr>
        ))}

        {opponentStats.map((player) => (
          <tr>
            {Object.values(player).map((stat) => (
              <td className="border-x border-black p-4"> {stat} </td>
            ))}
          </tr>
        ))}
      </table>
    </div>
  );
};

export default GameCard;
