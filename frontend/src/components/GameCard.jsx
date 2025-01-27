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
        <thead>
          <tr className="border border-black">
            {Object.keys(teamStats[0]).map((header, index) => (
              <th key={index} className="border border-black p-4">
                {header.toUpperCase()}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {teamStats.map((player, index) => (
            <tr key={`team-${index}`}>
              {Object.values(player).map((stat, i) => (
                <td
                  key={`team-${index}-stat-${i}`}
                  className="border-x border-black p-4"
                >
                  {stat}
                </td>
              ))}
            </tr>
          ))}

          {opponentStats.map((player, index) => (
            <tr key={`opponent-${index}`}>
              {Object.values(player).map((stat, i) => (
                <td
                  key={`opponent-${index}-stat-${i}`}
                  className="border-x border-black p-4"
                >
                  {stat}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default GameCard;
