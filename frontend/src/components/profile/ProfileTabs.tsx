"use client";

interface ProfileTabsProps {
    activeTab: string;
    onTabChange: (
        tab: string
    ) => void;
}

const tabs = [
    {
        id: "trips",
        label: "Trips",
        icon: "🗺️"
    },
    {
        id: "saved",
        label: "Saved",
        icon: "🔰"
    },
    {
        id: "achievements",
        label: "Achievements",
        icon: "🏆"
    }
];

export default function ProfileTabs({
    activeTab,
    onTabChange
}: ProfileTabsProps) {
    return (
        <section
            style={{
                maxWidth: "1100px",
                margin: "0 auto 30px auto"
            }}
        >
            <div
                className="glass-card"
                style={{
                    padding: "10px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent:
                        "center",
                    gap: "12px",
                    flexWrap: "wrap"
                }}
            >
                {tabs.map(
                    (tab) => {
                        const isActive =
                            activeTab ===
                            tab.id;

                        return (
                            <button
                                key={
                                    tab.id
                                }
                                onClick={() =>
                                    onTabChange(
                                        tab.id
                                    )
                                }
                                style={{
                                    border:
                                        "none",
                                    cursor:
                                        "pointer",

                                    display:
                                        "flex",

                                    alignItems:
                                        "center",

                                    gap: "8px",

                                    padding:
                                        "14px 24px",

                                    borderRadius:
                                        "999px",

                                    fontWeight:
                                        700,

                                    fontSize:
                                        "0.95rem",

                                    transition:
                                        "all 0.3s ease",

                                    background:
                                        isActive
                                            ? "linear-gradient(135deg,#0EA5E9,#14B8A6)"
                                            : "rgba(255,255,255,0.05)",

                                    color:
                                        isActive
                                            ? "#ffffff"
                                            : "#CBD5E1",

                                    boxShadow:
                                        isActive
                                            ? "0 0 25px rgba(14,165,233,0.35)"
                                            : "none"
                                }}
                            >
                                <span>
                                    {
                                        tab.icon
                                    }
                                </span>

                                <span>
                                    {
                                        tab.label
                                    }
                                </span>
                            </button>
                        );
                    }
                )}
            </div>
        </section>
    );
}