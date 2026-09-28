import { useCallback, useEffect, useState } from "react";
import type { Sound } from "../../types";
import { formatKey, getBindForFile } from "../../utils";
import { toast } from "../ui/Toast";

interface Props {
  sounds: Sound[];
  hotkeys: Record<string, string>;
  onUpdate: (hotkeys: Record<string, string>) => void;
}

// ⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀
// ⠀⠀⠀⠀⠀⠀⡼⠁⠈⠑⠲⣒⠂⠉⠓⠒⢤⠞⠉⠲⡉⠙⡄⠀⠀⠀
// ⠀⠀⠀⠀⣠⢾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⡎⠀⡔⡰⠛⠲⡜⢢⡀⠀
// ⠀⠀⢀⡜⠁⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣄⠈⣧⡀⢠⣏⢆⠇⠀
// ⠀⠀⡞⠀⠀⠉⠀⠀⠀⠀⢀⠄⠤⡀⠀⠀⠀⠈⠉⠀⠈⠑⠤⡊⠀⠀
// ⠰⢦⡧⠤⢄⣀⠀⠀⠀⠐⠁⠀⠀⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⣀⡀
// ⠀⠀⡇⠀⠀⢸⣍⠀⠀⠀⠀⣠⣄⠈⠾⠀⠀⠀⠠⣆⣠⠜⢉⡇⡀⠀
// ⢀⡤⠿⡖⠋⠉⠙⣷⡀⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠸⠟⠠⣔⡁⠀⠁
// ⠈⠁⠀⠳⣄⡠⠔⠉⢷⣄⠀⠙⠋⠀⠀⠀⢰⡶⠀⠀⣀⡴⠛⠓⢦⠀
// ⠀⠀⠀⢠⠞⠳⢤⣀⠀⢹⣶⣶⣶⣶⣴⣶⣾⣾⣿⡟⣿⠇⠀⠀⢸⠀
// ⠀⠀⠀⠁⠀⠀⢀⠞⠉⢹⣿⣯⣿⣯⣞⣿⡿⠉⠛⢿⠁⠀⠀⠀⡜⠀
// ⠀⠀⠀⠀⠀⣠⢋⡀⠀⡆⠙⠛⠛⠛⠛⠋⠀⠀⠀⠀⡲⠀⠂⠚⠁⠀
// ⠀⠀⠀⠀⠰⠁⠀⠀⠉⠣⡀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀
// ⠀⠀⠀⠀⠈⢄⠀⢀⡴⠚⠁⠀⠀⠀⠀⠀⠀⢀⢴⠁⠀⠀⠀⠀⠀⠀
// ⠀⠀⠀⠀⠀⠀⠈⠹⡀⠀⠀⠀⠀⢀⣠⢔⣊⠥⢺⠀⠀⠀⠀⠀⠀⠀
// ⠀⠀⠀⠀⠀⠀⠀⠀⠱⣀⠀⠀⢀⠠⢸⠈⠒⠐⠁⠀⠀⠀⠀⠀⠀⠀
// ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠲⠤⠤⠔⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

export function BindsTab({ sounds, hotkeys, onUpdate }: Props) {
  const [listening, setListening] = useState<string | null>(null);

  const handleKey = useCallback(
    (e: KeyboardEvent) => {
      if (!listening) return;
      e.preventDefault();
      if (e.key === "Escape") {
        setListening(null);
        return;
      }

      const code = e.code;
      const next = { ...hotkeys };
      for (const [k, f] of Object.entries(next)) {
        if (k === code || f === listening) delete next[k];
      }
      next[code] = listening;
      setListening(null);
      onUpdate(next);
      toast(`bound: ${formatKey(code)}`, "success");
    },
    [listening, hotkeys, onUpdate],
  );

  useEffect(() => {
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [handleKey]);

  const clearBind = (file: string) => {
    const next = { ...hotkeys };
    for (const [k, f] of Object.entries(next)) {
      if (f === file) delete next[k];
    }
    onUpdate(next);
  };

  if (!sounds.length) return <div className="empty">no sounds</div>;

  return (
    <>
      <div className="binds-hint">
        click the key field, then press a key to assign a bind
      </div>
      <div className="bind-list">
        {sounds.map((s) => {
          const bind = getBindForFile(hotkeys, s.file);
          return (
            <div className="bind-row" key={s.file}>
              <div className="bind-name">
                {s.name}
                <span className="bind-ext">{s.ext}</span>
              </div>
              <div
                className={`bind-key ${listening === s.file ? "listening" : ""}`}
                onClick={() =>
                  setListening(listening === s.file ? null : s.file)
                }
              >
                {listening === s.file ? "..." : bind ? formatKey(bind) : "—"}
              </div>
              <button className="bind-clear" onClick={() => clearBind(s.file)}>
                ×
              </button>
            </div>
          );
        })}
      </div>
    </>
  );
}
